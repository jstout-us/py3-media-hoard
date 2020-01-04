from datetime import datetime

import pytest

from dateutil import tz
from django.conf import settings


def pytest_configure():
    settings.configure(
        INSTALLED_APPS = ('media_hoard.data',),
        SECRET_KEY = 'REPLACE_ME',
        DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    }
                }
            )


@pytest.fixture
def fix_btb_uri():
    return 'tests/_fixtures/feeds/behind_the_bastards.rss'


@pytest.fixture
def fix_btb_channel(fix_btb_uri):
    summary = "<p>There’s a reason the History Channel has produced hundreds of documentaries about Hitler but only a few about Dwight D. Eisenhower. Bad guys (and gals) are eternally fascinating. Behind the Bastards dives in past the Cliffs Notes of the worst humans in history and exposes the bizarre realities of their lives. Listeners will learn about the young adult novels that helped Hitler form his monstrous ideology, the founder of Blackwater’s insane quest to build his own Air Force, the bizarre lives of the sons and daughters of dictators and Saddam Hussein’s side career as a trashy romance novelist.</p>"
    uri_icon = "https://megaphone-prod.s3.amazonaws.com/podcasts/22c36480-3778-11e8-806d-cfb84f1d0648/image/uploads_2F1547069138516-4edafwuejvc-14cc4c048140986ac2bacd6b0e0f022d_2FBehindTheBastards-Logo-iHR-FINAL-3000x3000.jpg"

    fixture = {
        'title': "Behind the Bastards",
        'subtitle': "Everything you don't know about History's greatest monsters",
        'author': "iHeartRadio",
        'language': "en",
        'publisher': "iHeartRadio (applepodcast@howstuffworks.com)",
        'summary': summary,
        'uri_site': 'https://www.behindthebastards.com/',
        'uri_feed': fix_btb_uri,
        'uri_image': uri_icon,
        'items': 173,
        }

    return fixture


@pytest.fixture
def fix_btb_item():
    fixture = {
        'title': "Part One; The Idiot Who Made, And Destroyed, WeWork",
        'subtitle': "",
        'author': "iHeartRadio",
        'duration': 5171,
        'time_published': datetime(2019, 12, 17, 11, 0, tzinfo=tz.UTC),
        'guid': "79f9cf16-a33b-11e9-949e-eb7c74e06cee",
        'guid_is_uri': False,
        'uri_src': 'https://www.podtrac.com/pts/redirect.mp3/chtbl.com/track/5899E/traffic.megaphone.fm/HSW7013309724.mp3',
        'file_type': 'audio/mpeg',
        }

    return fixture
