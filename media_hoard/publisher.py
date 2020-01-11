# -*- coding: utf-8 -*-

"""Module Media Hoard.publisher."""
import operator

from datetime import datetime

import feedparser

from dateutil import parser
from dateutil import tz


def _get_uri_src(links):
    for link in links:
        if '.mp3' in link['href']:
            return (link['href'], link['type'])

    return (None, None)


def _normalize_duration(value):
    multipliers = [1, 60, 60*60]
    elements = [int(x) for x in value.split(':')]
    elements.reverse()

    return sum([operator.mul(x, y) for (x, y) in zip(multipliers, elements)])


def _normalize_item(entry):
    """Normailize feed entry data.

    Args:
        entry(dict):    Entry dictionary from feedparser

    Returns:
        item(dict):     Normalized item data.
    """
    uri_src, file_type = _get_uri_src(entry['links'])
    item = {
        'title': entry['title'],
        'subtitle': entry['subtitle'],
        'author': entry['author'],
        'duration': _normalize_duration(entry['itunes_duration']),
        'time_published': parser.parse(entry['published']),
        'guid': entry['id'],
        'guid_is_uri': entry['guidislink'],
        'uri_src': uri_src,
        'file_type': file_type,
        }

    return item


def get_feed(src, **kwargs):
    """Retreive and parse channel feed.

    Args:
        src(str):   url or file path to channel feed file.

    Kwargs:
        newest(datetime):   Newest item publish date to add
        oldest(datetime):   Oldest item publish date to add

    Returns:
        channel(dict):  The channel information dictionary
        items(list):    List of channel item dictionaries
    """
    newest = kwargs.get('newest', datetime(9999, 12, 31, 0, 0, 0, tzinfo=tz.UTC))
    oldest = kwargs.get('oldest', datetime(1, 1, 1, 0, 0, 0, tzinfo=tz.UTC))

    feed = feedparser.parse(src, )
    items = [_normalize_item(x) for x in feed.pop('entries')]
    items = [x for x in items if oldest <= x['time_published'] <= newest]

    publisher = '{} ({})'.format(feed['feed']['author_detail']['name'],
                                 feed['feed']['author_detail']['email'])

    channel = {
        'title': feed['feed']['title'],
        'subtitle': feed['feed']['subtitle'],
        'summary': feed['feed'].get('summary', ''),
        'author': feed['feed']['author'],
        'publisher': publisher,
        'language': feed['feed']['language'],
        'uri_site': feed['feed']['link'],
        'uri_feed': src,
        'uri_image': feed['feed']['image']['href'],
        'items': len(items)
        }

    return (channel, items)
