# -*- coding: utf-8 -*-

"""Test module doc string."""
import os

import pytest
import subprocess

import media_hoard


def test_accept_sub_rss(tmp_path):
    env = os.environ.copy()
    env['MH_DATA_ROOT'] = str(tmp_path)
    env['HOME'] = '/home/user'

    # First run of application
    expected = 'Initialize DB\nSubscribed to channel - Behind the Bastards (173 Items)\n'
    args = [
        'media-hoard',
        'subscribe',
        'http://liberator/podcasts/behind-the-bastards/channel.rss'
        ]

    result = subprocess.check_output(args=args, encoding='utf-8', env=env)
    assert expected == result
    assert (tmp_path / 'db.sqlite').is_file()

    # Duplicate subscription
    expected = 'Already subscribed to channel - Behind the Bastards\n'
    result = subprocess.check_output(args=args, encoding='utf-8', env=env)
    assert expected == result

     # Test bad URL
    expected = 'Subscription failed - Failed to retreive or parse feed\n'
    args[-1] = 'http://liberator/podcasts/no-such-podcast/channel.rss'
    result = subprocess.check_output(args=args, encoding='utf-8', env=env)
    assert expected == result
