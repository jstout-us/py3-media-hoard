# -*- coding: utf-8 -*-

"""Test module doc string."""
import pytest

from media_hoard import api
from media_hoard import publisher


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
