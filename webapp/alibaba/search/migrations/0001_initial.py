# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name='\u5206\u7c7b\u540d\u79f0')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='\u522b\u540d')),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('order', models.SmallIntegerField(default=0, verbose_name='\u5e8f\u53f7')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('parent',
                 models.ForeignKey(verbose_name='\u7236\u5206\u7c7b', blank=True, to='search.Category', null=True)),
            ],
            options={
                'ordering': ('order',),
                'get_latest_by': 'created',
                'verbose_name': '\u641c\u7d22\u5206\u7c7b',
                'verbose_name_plural': '\u641c\u7d22\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name='\u5206\u7c7b\u540d\u79f0')),
                ('picture',
                 models.ImageField(upload_to=b'photos', width_field=100, height_field=100, blank=True, null=True,
                                   verbose_name='\u56fe\u7247')),
                ('url', models.URLField(verbose_name='\u8fde\u63a5')),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('order', models.SmallIntegerField(default=0, verbose_name='\u5e8f\u53f7')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ('order',),
                'get_latest_by': 'created',
                'verbose_name': '\u53cb\u60c5\u8fde\u63a5',
                'verbose_name_plural': '\u53cb\u60c5\u8fde\u63a5',
            },
        ),
    ]
