# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-13 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('author_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('actual_price', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('description', tinymce.models.HTMLField(null=True)),
                ('discount', models.PositiveIntegerField(null=True)),
                ('rating', models.BooleanField(default=True)),
                ('url', models.URLField(blank=True)),
                ('paperback', models.IntegerField(null=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media_root/books/')),
                ('image_height', models.PositiveIntegerField(blank=True, default='100', editable=False, null=True)),
                ('image_width', models.PositiveIntegerField(blank=True, default='100', editable=False, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.BookDetails')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media_root/books/')),
                ('image_height', models.PositiveIntegerField(blank=True, default='100', editable=False, null=True)),
                ('image_width', models.PositiveIntegerField(blank=True, default='100', editable=False, null=True)),
                ('category_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Category')),
            ],
        ),
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.MainCategory'),
        ),
        migrations.AddField(
            model_name='category',
            name='default',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_main_category', to='books.MainCategory'),
        ),
        migrations.AddField(
            model_name='bookdetails',
            name='Main_Category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='books.MainCategory'),
        ),
        migrations.AddField(
            model_name='bookdetails',
            name='categories',
            field=models.ManyToManyField(blank=True, to='books.Category'),
        ),
        migrations.AddField(
            model_name='bookdetails',
            name='default',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_category', to='books.Category'),
        ),
        migrations.AddField(
            model_name='bookdetails',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
