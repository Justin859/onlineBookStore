# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 12:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20170623_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='author_writing_style',
            new_name='author_info',
        ),
    ]