# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-16 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20161230_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='readerbookcard',
            name='bookcopy_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookcopyincard', to='library.BookCopy'),
        ),
    ]
