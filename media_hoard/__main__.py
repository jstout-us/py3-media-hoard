# -*- coding: utf-8 -*-

"""Entry point for media_hoard."""
import os
import sys

from pathlib import Path

import click
import django

from django.conf import settings
from django.core.management import execute_from_command_line

# from . import api
from . import config

def setup():
    data_root = Path(config.get_data_root())
    db_path = data_root / 'db.sqlite'

    settings.configure(
        INSTALLED_APPS = ('media_hoard.data',),
        SECRET_KEY = 'REPLACE_ME',
        DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': str(db_path)
                    }
                }
            )

    if not db_path.is_file():
        print('Initialize DB')
        store = sys.stdout
        with open(os.devnull, 'w') as fd_null:
            sys.stdout = fd_null
            argv = ['manage.py', 'migrate']
            execute_from_command_line(argv)

        sys.stdout = store

    django.setup()



def cleanup():
    pass


@click.group()
def cli():
    pass


@cli.command()
@click.argument('url')
def subscribe(url):
    setup()
    from . import api

    try:
        title, items = api.subscribe(url)
        click.echo('Subscribed to channel - {} ({} Items)'.format(title, items))

    except api.SubscriptionExistsError as exc:
        click.echo('Already subscribed to channel - {}'.format(exc))

    finally:
        cleanup()
