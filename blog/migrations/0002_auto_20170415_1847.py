# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-15 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategoryimage',
            name='image',
            field=models.ImageField(upload_to='media_root/blog/'),
        ),
        migrations.AlterField(
            model_name='blogimage',
            name='image',
            field=models.ImageField(upload_to='media_root/blog/'),
        ),
    ]