# -*- coding: utf-8 -*-

"""Module Media Hoard.api"""
from django.db.utils import IntegrityError

from . import publisher
from media_hoard.data.models import Channel


class SubscriptionExistsError(Exception):
    """Channel subscription exists."""


def subscribe(src):
    """
    """

    feed_data, _ = publisher.get_feed(src)
    items = feed_data.pop('items')

    try:
        channel = Channel.objects.create(**feed_data)           # pylint: disable=no-member

    except IntegrityError:
        raise SubscriptionExistsError(feed_data['title'])

    return (channel.title, items)
