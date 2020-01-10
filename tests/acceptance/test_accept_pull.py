# -*- coding: utf-8 -*-

"""Test module doc string."""
import os

from pathlib import Path

import pytest
import subprocess

from . import commands


@pytest.fixture
def exp_pull_1():
    """Return expected STDOUT from first pull run."""
    with Path('tests/_fixtures/accept_pull_output_first.txt').open() as fd_in:
        return fd_in.read()


@pytest.fixture
def exp_pull_2():
    """Return expcted STDOUT from second pull run."""
    with Path('tests/_fixtures/accept_pull_output_second.txt').open() as fd_in:
        return fd_in.read()


def test_accept_pull_channels(fix_env, fix_uri_btb, fix_uri_tam, exp_pull_1, exp_pull_2):
    for uri in [fix_uri_btb, fix_uri_tam]:
        commands.channel_sub(fix_env, uri)

    args = [
        'media-hoard',
        'pull',
        '--oldest',
        '2019-12-09',
        '--newest',
        '2019-12-16'
        ]
    result = subprocess.check_output(args=args, encoding='utf-8', env=fix_env)
    assert exp_pull_1 == result

    args = [
        'media-hoard',
        'pull',
        '--oldest',
        '2019-12-09'
        ]
    result = subprocess.check_output(args=args, encoding='utf-8', env=fix_env)
    assert exp_pull_2 == result

    pub_files = [
        'Behind the Bastards/20191217 - Part One; The Idiot Who Made, And Destroyed, WeWork.mp3',
        'Behind the Bastards/20191212 - The School That Raped Everbody.mp3',
        'Behind the Bastards/20191210 - Part Three: Jerry Falwell: Founder of the Religious Right.mp3',
        'This American Life/20191229 - 690: Too Close to Home.mp3',
        'This American Life/20191222 - 576: Say Yes To Christmas.mp3',
        'This American Life/20191215 - 323: The Super.mp3',
        ]

    for pub_file in pub_files:
        assert (Path(fix_env['MH_PUBLISH_ROOT']) / pub_file).is_symlink()
