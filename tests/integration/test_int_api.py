# -*- coding: utf-8 -*-

"""Test module doc string."""
import os

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
            'hash_sha1': '93931086528aa8631718ed3d1f98e9914f121ee1',
            'state': 'OK',
            'symlink_name': 'Podcast Channel 1/20191212 - Older Podcast Episode.mp3'
            },
        {
            'title': 'Latest Podcast Episode',
            'hash_sha1': '03268bb13baa9d277e15cc1b15d7b6457f3072d5',
            'state': 'OK',
            'symlink_name': 'Podcast Channel 1/20191217 - Latest Podcast Episode.mp3'
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


@pytest.mark.django_db(transaction=True)
def test_channel_pull(tmp_path, settings, exp_items, fix_channel, fix_items):
    media_root = tmp_path / 'items'
    media_root.mkdir()
    settings.MEDIA_ROOT = str(media_root)

    pub_root = tmp_path / 'pub'
    pub_root.mkdir()

    patch_dict = {'HOME': '/home/user', 'MH_PUBLISH_ROOT': str(pub_root)}
    patch_pull = 'media_hoard.publisher.get_feed'
    pull_1_retval = (fix_channel, fix_items[-1:])
    pull_2_retval = (fix_channel, fix_items)

    channel = models.Channel.objects.create(**fix_channel)

    with mock.patch.dict(os.environ, patch_dict):
        with mock.patch(patch_pull, return_value=pull_1_retval) as mocked:
            api.pull()
            assert models.Item.objects.all().count() == 1

        with mock.patch(patch_pull, return_value=pull_2_retval) as mocked:
            api.pull()
            assert models.Item.objects.all().count() == 2

    for count, item in enumerate(models.Item.objects.all()):
        assert channel == item.channel
        assert exp_items[count]['title'] == item.title
        assert exp_items[count]['hash_sha1'] == item.hash_sha1
        assert exp_items[count]['state'] == item.state
        assert (media_root / item.file.name).is_file()
        assert (pub_root / exp_items[count]['symlink_name']).is_symlink()
