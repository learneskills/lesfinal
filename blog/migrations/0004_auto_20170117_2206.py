# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-17 16:36
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170117_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogdetail',
            name='description',
            field=tinymce.models.HTMLField(null=True),
        ),
    ]
