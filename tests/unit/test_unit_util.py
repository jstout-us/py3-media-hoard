# -*- coding: utf-8 -*-

"""Test module doc string."""
from pathlib import Path

import pytest

from media_hoard import util


@pytest.fixture
def fix_path():
    """Return path to ficture file."""
    return 'tests/_fixtures/files/item_1.mp3'


def test_copy_file(tmp_path, fix_path):
    expected = 'item_1.mp3\n'

    tmp_file = tmp_path / "test_copy_file_1.mp3"

    with tmp_file.open('w+b') as fd_tmp:
        util.copy_file(fix_path, fd_tmp)
        fd_tmp.seek(0)

        assert expected == fd_tmp.read().decode()


def test_hash_file(fix_path):
    expected = '03268bb13baa9d277e15cc1b15d7b6457f3072d5'

    with Path(fix_path).open('rb') as fd_fix:
        hash_ = util.hash_file(fd_fix)

        assert expected == hash_


def test_format_duration():
    duration = 3630
    expected = '01:00:30'

    result = util.format_duration(duration)

    assert expected == result
