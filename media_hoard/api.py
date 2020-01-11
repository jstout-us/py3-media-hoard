# -*- coding: utf-8 -*-

"""Module Media Hoard.api."""
import tempfile
from pathlib import Path

from django.db.utils import IntegrityError
from django.conf import settings
from django.core.files import File

from . import config
from . import publisher
from . import util
from .data import models


class FeedParseError(Exception):
    """Channel subscription exists."""


class SubscriptionExistsError(Exception):
    """Channel subscription exists."""


def pull(**kwargs):
    """Pull and save new items from all subscribed channels.

    Kwargs:
        newest(datetime):   Newest item publish date to add
        oldest(datetime):   Oldest item publish date to add

    Returns:
        None
    """
    for channel in models.Channel.objects.all():                                    # pylint: disable=no-member
        _, feed_items = publisher.get_feed(channel.uri_feed, **kwargs)
        print('Pull feed from {} [ OK ]'.format(channel.title))

        for feed_item in feed_items:
            try:
                item = models.Item.objects.create(channel=channel, **feed_item)     # pylint: disable=no-member

            except IntegrityError:
                pass

    new_items = models.Item.objects.filter(state='QD').order_by('-time_published')  # pylint: disable=no-member
    new_item_count = new_items.count()

    for count, item in enumerate(new_items, start=1):
        with tempfile.TemporaryFile() as fd_tmp:
            util.copy_file(item.uri_src, fd_tmp)
            fd_tmp.seek(0)

            item.hash_sha1 = util.hash_file(fd_tmp)
            fd_tmp.seek(0)

            item_file = File(fd_tmp)
            item.file.save(item.hash_sha1 + '.mp3', item_file, save=True)
            item.state = 'OK'
            item.save()

            target = Path(settings.MEDIA_ROOT) / item.file.name
            pub_dir = Path(config.get_publish_root()) / item.channel.title
            pub_dir.mkdir(exist_ok=True)

            name = '{} - {}.{}'.format(item.time_published.strftime('%Y%m%d'),
                                       item.title,
                                       item.format)

            (pub_dir / name).symlink_to(target)

        print('Pull item {}/{} - {} - {} ({}) [ {} ]'.format(count,
                                                             new_item_count,
                                                             item.channel.title,
                                                             item.title,
                                                             util.format_duration(item.duration),
                                                             item.state))


def subscribe(src):
    """Subscribe to channel using feed document located at src.

    Args:
        src(str):       url or file path

    Returns:
        title(str):     Channel title
        items(int):     Number of channel item/entry items
    """
    try:
        feed_data, _ = publisher.get_feed(src)
        items = feed_data.pop('items')

    except KeyError:
        raise FeedParseError

    try:
        channel = models.Channel.objects.create(**feed_data)           # pylint: disable=no-member

    except IntegrityError:
        raise SubscriptionExistsError(feed_data['title'])

    return (channel.title, items)
