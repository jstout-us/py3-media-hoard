# -*- coding: utf-8 -*-

"""Test module doc string."""

import pytest
import subprocess

import media_hoard


def test_accept_sub_rss():
    expected = 'Subscribed to channel - Behind the Bastards\n'
    args = [
        'media-hoard',
        'subscribe',
        'http://liberator/podcasts/behind-the-bastards/channel.rss'
        ]

    result = subprocess.check_output(args).decode()
    print(result)

    assert expected == result
