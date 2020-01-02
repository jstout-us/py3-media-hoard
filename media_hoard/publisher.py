# -*- coding: utf-8 -*-

"""Module Media Hoard.publisher"""

import feedparser

from dateutil import parser


def _normalize_item(entry):
    """Normailize feed entry data.

    Args:
        entry(dict):    Entry dictionary from feedparser

    Returns:
        item(dict):     Normalized item data.
    """
    item = {
        'title': entry['title'],
        'subtitle': entry['subtitle'],
        'author': entry['author'],
        'duration': int(entry['itunes_duration']),
        'time_published': parser.parse(entry['published']),
        'guid': entry['id'],
        'guid_is_uri': entry['guidislink'],
        'uri_src': entry['links'][0]['href'],
        'file_type': entry['links'][0]['type'],
        }

    return item


def get_feed(src):
    """Retreive and parse channel feed.

    Args:
        src(str):   url or file path to channel feed file.

    Returns:
        channel(dict):  The channel information dictionary
        items(list):    List of channel item dictionaries
    """
    feed = feedparser.parse(src)

    items = [_normalize_item(x) for x in feed.pop('entries')]

    publisher = '{} ({})'.format(feed['feed']['publisher_detail']['name'],
                                 feed['feed']['publisher_detail']['email'])

    channel = {
        'title': feed['feed']['title'],
        'subtitle': feed['feed']['subtitle'],
        'summary': feed['feed']['summary'],
        'author': feed['feed']['author'],
        'publisher': publisher,
        'language': feed['feed']['language'],
        'uri_site': feed['feed']['link'],
        'uri_feed': src,
        'uri_image': feed['feed']['image']['href'],
        'items': len(items)
        }

    return (channel, items)
