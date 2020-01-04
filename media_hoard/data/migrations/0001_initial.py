# noqa
# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-01-02 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration): # noqa
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('subtitle', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('summary', models.TextField()),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('title',), unique=True)),
                ('author', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=10)),
                ('time_added', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_qa_checked', models.BooleanField(default=False)),
                ('uri_site', models.URLField()),
                ('uri_feed', models.URLField()),
                ('uri_icon', models.URLField(blank=True, default=None, null=True)),
                ('uri_image', models.URLField(blank=True, default=None, null=True)),
            ],
        ),
    ]