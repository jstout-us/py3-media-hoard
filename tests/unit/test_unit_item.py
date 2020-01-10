# -*- coding: utf-8 -*-

"""Test module doc string."""

import pytest

from django.db.utils import IntegrityError

from media_hoard.data import models


@pytest.mark.django_db
def test_item_init(fix_btb_channel, fix_btb_item):
    fix_btb_channel.pop('items')
    channel = models.Channel.objects.create(**fix_btb_channel)

    item = models.Item.objects.create(channel=channel, **fix_btb_item)
    assert item.id
    assert item.time_added
    assert item.format == 'mp3'
    assert item.hash_sha1 == ''
    assert item.state == 'QD'

    with pytest.raises(IntegrityError):
        models.Item.objects.create(channel=channel, **fix_btb_item)
