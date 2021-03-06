# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_bookcartitems_item_checked_out'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_pk', models.IntegerField()),
                ('item_id', models.IntegerField()),
                ('item_title', models.CharField(max_length=255)),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('item_quantity', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='bookcartitems',
            options={},
        ),
        migrations.RemoveField(
            model_name='bookcartitems',
            name='item_checked_out',
        ),
    ]
