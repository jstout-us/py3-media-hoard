#!/usr/bin/python3
"""
Clone a remote podcast to our local fixture server for testing use.

Known Issues/Limitations:

1.  All files downloaded to /tmp/ first and then copied to media fix dir; if we crash during job
    all progress to date is lost and we have to start over.

2.  A podcast with a large back catalog can fill VM partition and you should use an external
    server for tmp spool.

3.  Currently hardcoded to only pull from the behind-the-bastards rss feed in _fixtures
"""
import collections
import hashlib
import logging
import os
import pickle
import shutil
import sys
import tempfile
import time

from pathlib import Path

import requests
import feedparser

from dateutil import parser

FIX_ROOT = "/vagrant_data/"
HASH_TYPE = "sha1"
# URI_FEED = "tests/_fixtures/feeds/behind_the_bastards.rss"
URI_FEED = "tests/_fixtures/feeds/this_american_life.rss"
LOG_LEVEL = logging.DEBUG
BUF_SIZE = 65536

from pprint import pprint as pp


def _get_entry(dir_tmp, uri):
    tmp_file = _get_tmp_file(dir_tmp)

    with requests.get(uri, stream=True) as resp:
        resp.raise_for_status()

        with tmp_file.open('wb') as fd_out:
            for chunk in resp.iter_content(chunk_size=BUF_SIZE):
                fd_out.write(chunk)

    return tmp_file


def _get_tmp_file(dir):
    fd_tmp, path = tempfile.mkstemp(dir=app['dir_tmp'])
    os.close(fd_tmp)

    return Path(path)


def _hash_file(file_path, hash_type):
    hash_ = hashlib.new(hash_type)

    with file_path.open('rb') as fd_in:
        while True:
            data = fd_in.read(BUF_SIZE)

            if not data:
                break

            hash_.update(data)

    return hash_.hexdigest()


# def _normalize_entries(raw_entry):
#     entry = {
#         'title': raw_entry['title'],
#         'subtitle': raw_entry['subtitle'],
#         'author': raw_entry['author'],
#         'duration': int(raw_entry['itunes_duration']),
#         'time_published': parser.parse(raw_entry['published']),
#         'guid': raw_entry['id'],
#         'guid_is_uri': raw_entry['guidislink'],
#         'uri_src': raw_entry['links'][0]['href'],
#         'file_type': raw_entry['links'][0]['type'],
#         }

#     return entry

def _normalize_entries(raw_entry):

    entry = {
        'title': raw_entry['title'],
        'subtitle': raw_entry['subtitle'],
        'author': raw_entry['author'],
        'duration': _parse_duration(raw_entry['itunes_duration']),
        'time_published': parser.parse(raw_entry['published']),
        'guid': raw_entry['id'],
        'guid_is_uri': raw_entry['guidislink'],
        'uri_src': raw_entry['links'][1]['href'],
        'file_type': raw_entry['links'][1]['type'],
        }

    return entry

def _parse_duration(duration):
    multipliers = [3600, 60, 1]
    elements = [int(x) for x in duration.split(':')]

    sum_ = 0

    for mult, element in zip(multipliers, elements):
        sum_ += mult * element

    return sum_


def _pickle_file(dir_tmp, data):
    tmp_file = _get_tmp_file(dir_tmp)

    with tmp_file.open('wb') as fd_out:
        pickle.dump(data, fd_out)

    return (tmp_file)


def _rewrite_fix_uri(dir_tmp, uri_feed, data):
    with uri_feed.open('r') as fd_in:
        feed_data = fd_in.read()

    for entry in data['entries']:
        feed_data = feed_data.replace(entry['uri_src'], entry['uri_fix'])

    tmp_file = _get_tmp_file(dir_tmp)
    with tmp_file.open('w') as fd_out:
        fd_out.write(feed_data)

    return tmp_file


def get_entries(app, data_feed):
    app['log'].debug('get_entries() - Enter')

    files = collections.defaultdict(dict)
    data_fix = data_feed.copy()
    data_fix['entries'] = []
    count_entry = len(data_feed['entries'])

    for count, entry in enumerate(data_feed['entries'], start=1):
        log_msg = 'Get entry {}/{} - {}'.format(count, count_entry, entry['title'])
        app['log'].info(log_msg)

        tmp_file = _get_entry(app['dir_tmp'], entry['uri_src'])
        hash_ = _hash_file(tmp_file, app['hash_type'])
        file_name = '{}.mp3'.format(hash_)

        key = 'entry_{}'.format(count)
        files[key]['src'] = tmp_file
        files[key]['dst'] = app['dir_fix_media'] / file_name

        entry_fix = entry.copy()
        entry_fix['uri_fix'] = 'http://liberator/podcasts/{}/{}'.format(data_feed['slug'],
                                                                        file_name)
        entry_fix['hash'] = hash_

        data_fix['entries'].append(entry_fix)

        time.sleep(app['delay_get'])

    app['log'].debug('get_entries() - Exit')

    return (data_fix, files)


def get_feed(dir_tmp, uri_feed):
    """Download, parse and return normalized feed data.

    Args:
        uri_feed (str): uri for the feed source

    Raises:
        None

    Returns:
        feed_data (dict)
    """
    tmp_file = _get_tmp_file(dir_tmp)
    shutil.copy(uri_feed, tmp_file)

    feed = feedparser.parse(tmp_file)

    # data = {
    #     'title': feed['feed']['title'],
    #     'slug': feed['feed']['title'].lower().replace(' ', '-'),
    #     'subtitle': feed['feed']['subtitle'],
    #     'summary': feed['feed']['summary'],
    #     'author': feed['feed']['author'],
    #     'language': feed['feed']['language'],
    #     'uri_site': feed['feed']['link'],
    #     'uri_feed': uri_feed,
    #     'uri_image': feed['feed']['image']['href'],
    #     'entries': [_normalize_entries(x) for x in feed['entries']]
    #     }

    data = {
        'title': feed['feed']['title'],
        'slug': feed['feed']['title'].lower().replace(' ', '-'),
        'subtitle': feed['feed']['subtitle'],
        'author': feed['feed']['author'],
        'language': feed['feed']['language'],
        'uri_site': feed['feed']['link'],
        'uri_feed': uri_feed,
        'uri_image': feed['feed']['image']['href'],
        'entries': [_normalize_entries(x) for x in feed['entries']]
        }

    return (data, tmp_file)


def rewrite_feed(app, entries):
    app['log'].debug('rewrite_feed() - Enter')

    with app['file_fix_feed'].open('r') as fd_in:
        feed_data = fd_in.read()

    for count, entry in enumerate(entries, start=1):
        msg_log = 'replace uri {}/{} - {} -> {}'.format(count,
                                                        len(entries),
                                                        entry['uri_src'],
                                                        entry['uri_fix']
                                                        )

        app['log'].debug(msg_log)
        feed_data = feed_data.replace(entry['uri_src'], entry['uri_fix'])

    with app['file_fix_feed_rewrite'].open('w') as fd_out:
        fd_out.write(feed_data)

    app['log'].debug('rewrite_feed() - Exit')


def main(app, uri_feed):
    app['log'].debug('main() - Enter')

    fixtures = collections.defaultdict(dict)

    data_feed, fixtures['uri_feed']['src'] = get_feed(app['dir_tmp'], uri_feed)
    app['dir_fix_media'] = app['dir_fix_root'] / 'podcasts' / data_feed['slug']
    app['dir_fix_media'].mkdir(parents=True, exist_ok=True)

    fixtures['uri_feed']['dst'] = app['dir_fix_media'] / 'channel.rss.orig'

    fixtures['data_feed']['src'] = _pickle_file(app['dir_tmp'], data_feed)
    fixtures['data_feed']['dst'] = app['dir_fix_media'] / 'channel.pkl.orig'

    data_fix, entry_files = get_entries(app, data_feed)
    fixtures.update(entry_files)

    fixtures['data_fix']['src'] = _pickle_file(app['dir_tmp'], data_fix)
    fixtures['data_fix']['dst'] = app['dir_fix_media'] / 'channel.pkl'

    fixtures['data_feed_fix']['src'] = _rewrite_fix_uri(app['dir_tmp'],
                                                        fixtures['uri_feed']['src'],
                                                        data_fix
                                                        )
    fixtures['data_feed_fix']['dst'] = app['dir_fix_media'] / 'channel.rss'

    count_fix = len(fixtures)
    for key, value in fixtures.items():
        app['log'].info('Copy fixture: {} to media_root'.format(key))
        shutil.copy(value['src'], value['dst'])

    app['log'].debug('main() - Exit')


def setup(dir_fix_root, hash_type, log_level):
    formatter = logging.Formatter('%(message)s')
    handler_console = logging.StreamHandler()
    handler_console.setLevel(log_level)
    handler_console.setFormatter(formatter)

    log = logging.getLogger('make-fix')
    log.setLevel(log_level)
    log.addHandler(handler_console)

    dir_tmp = Path("/vagrant_data/tmp")
    dir_tmp.mkdir(parents=True, exist_ok=True)
    app = {
        'dir_fix_root': Path(dir_fix_root),
        'dir_fix_media': None,
        'dir_tmp': dir_tmp,
        'hash_type': hash_type,
        'log': log,
        'delay_get': 5,
        }

    app['log'].debug('temp dir: {}'.format(app['dir_tmp']))
    app['log'].debug('setup() - Exit')

    return app


def cleanup(app):

    app['log'].debug('cleanup() - Enter')

    app['log'].debug('Delete temp dir: {}'.format(app['dir_tmp']))
    shutil.rmtree(app['dir_tmp'])

    app['log'].debug('cleanup() - Exit')


if __name__ == '__main__':
    exit_code = 1
    app = {}

    try:
        app = setup(FIX_ROOT, HASH_TYPE, LOG_LEVEL)
        main(app, URI_FEED)
        sys.exit()

    except KeyboardInterrupt:
        app['log'].info('Intterupted by user')
        sys.exit()

    except Exception:
        app['log'].exception('Unhandled exception')
        sys.exit(1)

    finally:
        cleanup(app)

