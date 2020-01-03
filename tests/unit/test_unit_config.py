# -*- coding: utf-8 -*-

"""Test module doc string."""
import os

from unittest import mock

import pytest

from media_hoard import config


def test_get_data_root_default():
    expected = '/home/user/.local/share/jstout-us/media-hoard'

    assert expected == config.get_data_root()


@mock.patch.dict(os.environ,{'MH_DATA_ROOT': '/alt/path'})
def test_get_data_root_override():
    expected = '/alt/path'

    assert expected == config.get_data_root()
