# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-24 17:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0004_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_detail',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 2, 24, 17, 19, 48, 739670, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
