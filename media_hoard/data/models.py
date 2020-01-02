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
