# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20150911_2314'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u7b14\u8bb0\u540d\u79f0')),
                ('tag', models.CharField(max_length=255, verbose_name='\u7b14\u8bb0\u6807\u7b7e', blank=True)),
                ('note', models.TextField(verbose_name='\u7b14\u8bb0\u5185\u5bb9')),
                ('order', models.IntegerField(default=0)),
                ('search_enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u52a0\u5165\u641c\u7d22')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': '\u7528\u6237\u7b14\u8bb0',
                'verbose_name_plural': '\u7528\u6237\u7b14\u8bb0',
            },
        ),
        migrations.CreateModel(
            name='UserNoteBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u7b14\u8bb0\u540d\u79f0')),
                ('order', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('parent', models.ForeignKey(to='accounts.UserNoteBook', blank=True)),
                ('user', models.ForeignKey(related_name='notebook_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': '\u7528\u6237\u7b14\u8bb0\u672c',
                'verbose_name_plural': '\u7528\u6237\u7b14\u8bb0\u672c',
            },
        ),
        migrations.CreateModel(
            name='UserSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=255, verbose_name='\u641c\u7d20\u8bcd', db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('user', models.ForeignKey(related_name='search_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': '\u7528\u6237\u641c\u7d22\u5173\u952e\u8bcd',
                'verbose_name_plural': '\u7528\u6237\u641c\u7d22\u5173\u952e\u8bcd',
            },
        ),
        migrations.CreateModel(
            name='UserWebSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u540d\u79f0')),
                ('tag', models.CharField(max_length=255, verbose_name='\u6807\u7b7e', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('user', models.ForeignKey(related_name='website_user', to=settings.AUTH_USER_MODEL)),
                ('website', models.ForeignKey(related_name='user_website', to='scraper.Website')),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': '\u7528\u6237\u6536\u85cf\u7684\u7f51\u7ad9',
                'verbose_name_plural': '\u7528\u6237\u6536\u85cf\u7684\u7f51\u7ad9',
            },
        ),
        migrations.AddField(
            model_name='usernote',
            name='notebook',
            field=models.ForeignKey(verbose_name='\u7b14\u8bb0\u672c', to='accounts.UserNoteBook'),
        ),
        migrations.AddField(
            model_name='usernote',
            name='user',
            field=models.ForeignKey(related_name='note_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
