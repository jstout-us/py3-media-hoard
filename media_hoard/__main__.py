# -*- coding: utf-8 -*-

"""Entry point for media_hoard."""
import os
import sys

from pathlib import Path

import click
import django
from dateutil import tz
from django.conf import settings
from django.core.management import execute_from_command_line

from . import config


def setup():
    """Aapplication and Django setup."""
    data_root = Path(config.get_data_root())
    pub_root = Path(config.get_publish_root())

    media_root = data_root / 'items'

    db_path = data_root / 'db.sqlite'

    settings.configure(
        INSTALLED_APPS=('media_hoard.data',),
        SECRET_KEY='REPLACE_ME',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': str(db_path)
                }
            },
        TIME_ZONE='America/Los_Angeles',
        USE_TZ=True,
        MEDIA_ROOT=str(media_root)
        )

    if not db_path.is_file():
        print('Initialize DB')
        media_root.mkdir(parents=True)
        pub_root.mkdir(parents=True)

        store = sys.stdout
        with open(os.devnull, 'w') as fd_null:
            sys.stdout = fd_null
            argv = ['manage.py', 'migrate']
            execute_from_command_line(argv)

        sys.stdout = store

    django.setup()


@click.group()
def cli():
    """Command group."""


@cli.command()
@click.argument('url')
def subscribe(url):
    """Subscribe to podcast using feed document at url."""
    setup()
    from . import api   # pylint: disable=import-outside-toplevel

    try:
        title, items = api.subscribe(url)
        click.echo('Subscribed to channel - {} ({} Items)'.format(title, items))

    except api.SubscriptionExistsError as exc:
        click.echo('Already subscribed to channel - {}'.format(exc))

    except api.FeedParseError:
        click.echo('Subscription failed - Failed to retreive or parse feed')


@cli.command()
@click.option('--newest', default='9999-12-31', type=click.DateTime(),
              help="newest pubdate to pull")
@click.option('--oldest', default='1-1-1', type=click.DateTime(), help="oldest pubdate to pull")
def pull(newest, oldest):
    """Check all subscribed channels and add new items."""
    setup()
    from . import api   # pylint: disable=import-outside-toplevel

    newest = newest.replace(tzinfo=tz.UTC)
    oldest = oldest.replace(tzinfo=tz.UTC)

    api.pull(newest=newest, oldest=oldest)
