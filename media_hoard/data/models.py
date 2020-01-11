# -*- coding: utf-8 -*-

"""Module Media Hoard.podcasts.models."""

from django.db import models
from django_extensions.db.fields import AutoSlugField


class Channel(models.Model):
    """Podcast Channel Record."""

    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True, default='')
    summary = models.TextField()
    slug = AutoSlugField(max_length=50, unique=True, populate_from=('title',))

    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    language = models.CharField(max_length=10)

    time_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_qa_checked = models.BooleanField(default=False)

    uri_site = models.URLField()
    uri_feed = models.URLField()
    uri_icon = models.URLField(blank=True, null=True, default=None)
    uri_image = models.URLField(blank=True, null=True, default=None)


class Item(models.Model):
    """Podcast Item Record."""

    QUEUED = 'QD'
    OK = 'OK'
    WARN = 'WR'
    ERROR = 'ER'

    STATE_CHOICES = (
        (QUEUED, 'queued'),
        (OK, 'ok'),
        (WARN, 'warn'),
        (ERROR, 'error'),
        )

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True, default='')
    author = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    time_added = models.DateTimeField(auto_now_add=True)
    time_published = models.DateTimeField()
    guid = models.CharField(max_length=255)
    guid_is_uri = models.BooleanField()
    uri_src = models.URLField()
    file_type = models.CharField(max_length=25)
    hash_sha1 = models.CharField(max_length=40, default='')
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=QUEUED)
    file = models.FileField(null=True)
    channel = models.ForeignKey(Channel, related_name='items', on_delete=models.CASCADE)

    class Meta:                                     # pylint: disable=too-few-public-methods
        """For pylint."""

        unique_together = ['channel', 'guid']

    @property
    def format(self):
        """Return item format."""
        return "mp3"
