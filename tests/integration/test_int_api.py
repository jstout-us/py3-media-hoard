# -*- coding: utf-8 -*-

"""Test module doc string."""
from datetime import datetime
from unittest import mock

import pytest
from dateutil import tz

from media_hoard import api
from media_hoard import publisher
from media_hoard.data import models


@pytest.fixture
def fix_channel():
    fixture = {
        'title': 'Podcast Channel 1',
        'subtitle': 'Not a real channel',
        'summary': 'Integration Testing Fixture',
        'author': 'No such author',
        'publisher': 'No such publisher',
        'language': 'klingon',
        'uri_site': 'http://example.com',
        'uri_feed': 'http://example.com/feed.rss',
        'uri_image': 'http://example.com/img.jpg',
        }

    return fixture


@pytest.fixture
def fix_items():
    fixture = [
        {
            'title': 'Latest Podcast Episode',
            'subtitle': 'None',
            'author': 'No such author',
            'duration': 60,
            'time_published': datetime(2019, 12, 17, 11, 0, tzinfo=tz.UTC),
            'guid': '79f9cf16-a33b-11e9-949e-eb7c74e06cee',
            'guid_is_uri': False,
            'uri_src': 'tests/_fixtures/files/item_1.mp3',
            'file_type': 'audio/mpeg',
            },
        {
            'title': 'Older Podcast Episode',
            'subtitle': 'None',
            'author': 'No such author',
            'duration': 75,
            'time_published': datetime(2019, 12, 12, 11, 0, tzinfo=tz.UTC),
            'guid': '79f9cf16-949e-a33b-11e9-eb7c74e06cee',
            'guid_is_uri': False,
            'uri_src': 'tests/_fixtures/files/item_2.mp3',
            'file_type': 'audio/mpeg',
            }
    ]

    return fixture


@pytest.fixture
def exp_items():
    fixture = [
        {
            'title': 'Older Podcast Episode',
            'hash': '93931086528aa8631718ed3d1f98e9914f121ee1',
            'status': 'ok'
            },
        {
            'title': 'Latest Podcast Episode',
            'hash': '03268bb13baa9d277e15cc1b15d7b6457f3072d5',
            'status': 'ok'
            }
        ]

    return fixture


def test_get_feed_btb(fix_btb_uri, fix_btb_channel, fix_btb_item):
    channel, items = publisher.get_feed(fix_btb_uri)

    assert fix_btb_channel == channel
    assert fix_btb_item == items[0]


def test_get_feed_tal(fix_tal_uri, fix_tal_channel, fix_tal_item):
    channel, items = publisher.get_feed(fix_tal_uri)

    assert fix_tal_channel == channel
    assert fix_tal_item == items[0]


@pytest.mark.django_db
def test_subscribe_btb_rss(fix_btb_uri, fix_btb_channel):
    title, items = api.subscribe(fix_btb_uri)

    assert fix_btb_channel['title'] == title
    assert fix_btb_channel['items'] == items

    with pytest.raises(api.SubscriptionExistsError):
        api.subscribe(fix_btb_uri)

    with pytest.raises(api.FeedParseError):
        api.subscribe('path/to/no_such_fixture.rss')


@pytest.mark.django_db
def test_channel_pull(exp_items, fix_channel, fix_items):
    channel = models.Channel.objects.create(**fix_channel)

    with mock.patch('media_hoard.publisher.get_feed', return_value=fix_items[-1:]) as mocked:
        api.pull()
        assert models.Items.objects.all().count() == 1

    with mock.patch('media_hoard.publisher.get_feed', return_value=fix_items) as mocked:
        api.pull()
        assert models.Items.objects.all().count() == 2

    for count, item in enumerate(models.Items.objects.all()):
        assert channel == item.channel
        assert exp_items[count]['title'] == item.title
        assert exp_items[count]['hash'] == item.hash
        assert exp_items[count]['status'] == item.status
        assert item.file.path.is_file()
