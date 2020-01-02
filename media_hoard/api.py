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
    try:
        feed_data, _ = publisher.get_feed(src)
        items = feed_data.pop('items')

        channel = Channel(**feed_data)
        channel.save()

    except IntegrityError:
        raise SubscriptionExistsError

    return (channel.title, items)
