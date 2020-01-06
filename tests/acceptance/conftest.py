import os

import pytest


@pytest.fixture
def fix_env(tmp_path):
    """Return environ variables fixture for accept tests."""
    fixture = os.environ.copy()
    fixture['HOME'] = '/home/user'
    fixture['MH_DATA_ROOT'] = str(tmp_path / 'data')
    fixture['MH_PUB_ROOT'] = str(tmp_path / 'pub')

    return fixture


@pytest.fixture
def fix_uri_btb():
    """Return URI to local server Behind the Bastards feed fixture."""
    return 'http://liberator/podcasts/behind-the-bastards/channel.rss'


@pytest.fixture
def fix_uri_tam():
    """Return URI to local server This American Life feed fixture."""
    return 'http://liberator/podcasts/this-american-life/channel.rss'
