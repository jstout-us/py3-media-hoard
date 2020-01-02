# -*- coding: utf-8 -*-

"""Test module doc string."""
import pytest

from media_hoard import api
from media_hoard import publisher


def test_get_feed(fix_uri_rss, fix_channel_data, fix_item_data):
    channel, items = publisher.get_feed(fix_uri_rss)

    assert fix_channel_data == channel
    assert fix_item_data == items[0]


@pytest.mark.django_db
def test_subscribe_rss(fix_uri_rss, fix_channel_data):
    title, items = api.subscribe(fix_uri_rss)

    assert fix_channel_data['title'] == title
    assert fix_channel_data['items'] == items

    with pytest.raises(api.SubscriptionExistsError):
        api.subscribe(fix_uri_rss)
