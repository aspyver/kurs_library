# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20170116_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_in_stock_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]