# -*- coding: utf-8 -*-

"""Test module doc string."""

import pytest

from django.db.utils import IntegrityError

from media_hoard.data import models


@pytest.mark.django_db
def test_channel_init(fix_btb_channel):
    expected_slug = 'behind-the-bastards'
    fix_btb_channel.pop('items')

    channel = models.Channel.objects.create(**fix_btb_channel)

    assert channel.id
    assert channel.time_added
    assert channel.is_active
    assert not channel.is_qa_checked
    assert expected_slug == channel.slug

    with pytest.raises(IntegrityError):
        channel = models.Channel.objects.create(**fix_btb_channel)
