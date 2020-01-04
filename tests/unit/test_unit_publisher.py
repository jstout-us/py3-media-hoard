# -*- coding: utf-8 -*-

"""Test module doc string."""

import pytest

from media_hoard.publisher import _normalize_duration


def test_normalize_duration():
    values = [
        [3594, '00:59:54'],
        [5171, '5171']
        ]

    for expected, value in values:
        result = _normalize_duration(value)
        assert expected == result
