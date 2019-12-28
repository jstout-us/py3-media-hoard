# -*- coding: utf-8 -*-

"""Entry point for media_hoard."""

import sys

import click

import data


@click.group()
def cli():
    pass

@cli.command()
@click.argument('url')
def subscribe(url):
    channel = data.subscribe(url)
    click.echo('Subscribed to channel - {}'.format(channel.title))
