# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_auto_20170711_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditem',
            name='item_id',
            field=models.CharField(max_length=255),
        ),
    ]
