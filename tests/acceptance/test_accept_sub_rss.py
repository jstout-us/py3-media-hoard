# -*- coding: utf-8 -*-

"""Test module doc string."""
import os
from pathlib import Path

import pytest
import subprocess

from . import commands

def test_accept_sub_rss(fix_env, fix_uri_btb, fix_uri_tam):
    uri_bad ='http://liberator/podcasts/no-such-podcast/channel.rss'

    expected = 'Initialize DB\nSubscribed to channel - Behind the Bastards (173 Items)\n'
    result =  commands.channel_sub(fix_env, fix_uri_btb)
    assert expected == result
    assert (Path(fix_env['MH_DATA_ROOT']) / 'db.sqlite').is_file()

    # Duplicate subscription
    expected = 'Already subscribed to channel - Behind the Bastards\n'
    result =  commands.channel_sub(fix_env, fix_uri_btb)
    assert expected == result

    # Test bad URL
    expected = 'Subscription failed - Failed to retreive or parse feed\n'
    result =  commands.channel_sub(fix_env, uri_bad)
    assert expected == result

    # Second run of application
    expected = 'Subscribed to channel - This American Life (10 Items)\n'
    result =  commands.channel_sub(fix_env, fix_uri_tam)
    assert expected == result
