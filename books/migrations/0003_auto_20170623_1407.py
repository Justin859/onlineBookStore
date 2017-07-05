# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_bookcartitems'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=255)),
                ('author_description', models.TextField()),
                ('author_image', models.ImageField(max_length=255, upload_to=b'books/static/images/author-images')),
                ('author_writing_style', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='bookcartitems',
            options={'verbose_name': 'Book Cart', 'verbose_name_plural': 'Book Carts'},
        ),
        migrations.AlterField(
            model_name='bookcartitems',
            name='cart_item_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='bookcartitems',
            name='cart_pk',
            field=models.IntegerField(),
        ),
    ]