# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u5206\u7c7b\u540d\u79f0')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='\u522b\u540d')),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('order', models.SmallIntegerField(default=0, verbose_name='\u5e8f\u53f7')),
                ('hot', models.SmallIntegerField(default=0, verbose_name='\u70ed\u95e8')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('parent',
                 models.ForeignKey(verbose_name='\u7236\u5206\u7c7b', blank=True, to='scraper.Category', null=True)),
            ],
            options={
                'ordering': ('order',),
                'get_latest_by': 'created',
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='GeneralModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField()),
                ('thumbnail', models.CharField(max_length=200, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u901a\u7528\u6a21\u578b',
                'verbose_name_plural': '\u901a\u7528\u6a21\u578b',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=255)),
                ('ref_object', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=25, blank=True)),
                ('level', models.IntegerField(
                    choices=[(50, b'CRITICAL'), (40, b'ERROR'), (30, b'WARNING'), (20, b'INFO'), (10, b'DEBUG')])),
                ('spider_name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-date'],
                'verbose_name': '\u65e5\u5fd7',
                'verbose_name_plural': '\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='LogMarker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_contains', models.CharField(max_length=255)),
                ('ref_object', models.CharField(max_length=200, blank=True)),
                ('mark_with_type', models.CharField(
                    help_text=b'Choose "Custom" and enter your own type in the next field for a custom type',
                    max_length=2, choices=[(b'PE', b'Planned Error'), (b'DD', b'Dirty Data'), (b'IM', b'Important'),
                                           (b'IG', b'Ignore'), (b'MI', b'Miscellaneous'), (b'CU', b'Custom')])),
                ('custom_type', models.CharField(max_length=25, blank=True)),
                ('spider_name', models.CharField(max_length=200, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u65e5\u5fd7\u7279\u6027',
                'verbose_name_plural': '\u65e5\u5fd7\u7279\u6027',
            },
        ),
        migrations.CreateModel(
            name='Pipelines',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='\u522b\u540d')),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('conf', models.TextField(default=b'"HOST": 15,\n"PORT": 10080,\n', help_text='yaml\u683c\u5f0f',
                                          verbose_name='\u914d\u7f6e')),
                ('comments', models.TextField(verbose_name='\u4ecb\u7ecd', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': '\u7ba1\u9053',
                'verbose_name_plural': '\u7ba1\u9053',
            },
        ),
        migrations.CreateModel(
            name='SchedulerRuntime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('runtime_type',
                 models.CharField(default=b'P', max_length=1, choices=[(b'S', b'SCRAPER'), (b'C', b'CHECKER')])),
                ('next_action_time', models.DateTimeField(default=datetime.datetime.now)),
                ('next_action_factor', models.FloatField(null=True, blank=True)),
                ('num_zero_actions', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['next_action_time'],
                'verbose_name': '\u8fd0\u884c\u72b6\u6001',
                'verbose_name_plural': '\u8fd0\u884c\u72b6\u6001',
            },
        ),
        migrations.CreateModel(
            name='ScrapedObjAttr',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u5b57\u6bb5')),
                ('title', models.CharField(max_length=200, null=True, verbose_name='\u540d\u79f0', blank=True)),
                ('attr_type', models.CharField(max_length=1, choices=[(b'S', b'STANDARD'), (b'T', b'STANDARD (UPDATE)'),
                                                                      (b'B', b'BASE'), (b'U', b'DETAIL_PAGE_URL'),
                                                                      (b'I', b'IMAGE')])),
                ('id_field', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u5c5e\u6027',
                'verbose_name_plural': '\u5c5e\u6027',
            },
        ),
        migrations.CreateModel(
            name='ScrapedObjClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('scraper_scheduler_conf', models.TextField(
                    default=b'"MIN_TIME": 15,\n"MAX_TIME": 10080,\n"INITIAL_NEXT_ACTION_FACTOR": 10,\n"ZERO_ACTIONS_FACTOR_CHANGE": 20,\n"FACTOR_CHANGE_FACTOR": 1.3,\n')),
                ('checker_scheduler_conf', models.TextField(
                    default=b'"MIN_TIME": 1440,\n"MAX_TIME": 10080,\n"INITIAL_NEXT_ACTION_FACTOR": 1,\n"ZERO_ACTIONS_FACTOR_CHANGE": 5,\n"FACTOR_CHANGE_FACTOR": 1.3,\n')),
                ('comments', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Scraped\u7c7b\u578b',
                'verbose_name_plural': 'Scraped\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0')),
                ('slug', models.URLField(unique=True, max_length=100, verbose_name='\u522b\u540d', db_index=True)),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('status', models.CharField(default=b'P', max_length=1,
                                            choices=[(b'A', b'ACTIVE'), (b'M', b'MANUAL'), (b'P', b'PAUSED'),
                                                     (b'I', b'INACTIVE')])),
                ('content_type', models.CharField(default=b'H',
                                                  help_text=b'Data type format for scraped main pages (for JSON use JSONPath instead of XPath)',
                                                  max_length=1,
                                                  choices=[(b'H', b'HTML'), (b'X', b'XML'), (b'J', b'JSON')])),
                ('detail_page_content_type', models.CharField(default=b'H',
                                                              help_text=b'Data type format for detail pages and checker (for JSON use JSONPath instead of XPath)',
                                                              max_length=1, choices=[(b'H', b'HTML'), (b'X', b'XML'),
                                                                                     (b'J', b'JSON')])),
                ('render_javascript', models.BooleanField(default=False,
                                                          help_text=b'Render Javascript on pages (ScrapyJS/Splash deployment needed, careful: resource intense)')),
                ('max_items_read',
                 models.IntegerField(help_text=b'Max number of items to be read (empty: unlimited).', null=True,
                                     blank=True)),
                ('max_items_save',
                 models.IntegerField(help_text=b'Max number of items to be saved (empty: unlimited).', null=True,
                                     blank=True)),
                ('request_type', models.CharField(default=b'R',
                                                  help_text=b'Normal (typically GET) request (default) or form request (typically POST), using Scrapys corresponding request classes (not used for checker).',
                                                  max_length=1, choices=[(b'R', b'Request'), (b'F', b'FormRequest')])),
                ('method', models.CharField(default=b'GET', help_text=b'HTTP request via GET or POST.', max_length=10,
                                            choices=[(b'GET', b'GET'), (b'POST', b'POST')])),
                ('headers', models.TextField(
                    help_text=b'Optional HTTP headers sent with each request, provided as a JSON dict (e.g. {"Referer":"http://referer_url"}, use double quotes!)), can use {page} placeholder of pagination.',
                    blank=True)),
                ('body', models.TextField(
                    help_text=b'Optional HTTP message body provided as a unicode string, can use {page} placeholder of pagination.',
                    blank=True)),
                ('cookies', models.TextField(
                    help_text=b'Optional cookies as JSON dict (use double quotes!), can use {page} placeholder of pagination.',
                    blank=True)),
                ('meta', models.TextField(
                    help_text=b'Optional Scrapy meta attributes as JSON dict (use double quotes!), see Scrapy docs for reference.',
                    blank=True)),
                ('form_data', models.TextField(
                    help_text=b'Optional HTML form data as JSON dict (use double quotes!), only used with FormRequest request type, can use {page} placeholder of pagination.',
                    blank=True)),
                ('dont_filter', models.BooleanField(default=False,
                                                    help_text=b'Do not filter duplicate requests, useful for some scenarios with requests falsely marked as being duplicate (e.g. uniform URL + pagination by HTTP header).')),
                ('pagination_type', models.CharField(default=b'N', max_length=1,
                                                     choices=[(b'N', b'NONE'), (b'R', b'RANGE_FUNCT'),
                                                              (b'F', b'FREE_LIST')])),
                ('pagination_on_start', models.BooleanField(default=False)),
                ('pagination_append_str',
                 models.CharField(help_text=b'Syntax: /somepartofurl/{page}/moreurlstuff.html', max_length=200,
                                  blank=True)),
                ('pagination_page_replace', models.TextField(
                    help_text=b"RANGE_FUNCT: uses Python range funct., syntax: [start], stop[, step], FREE_LIST: 'Replace text 1', 'Some other text 2', 'Maybe a number 3', ...",
                    blank=True)),
                ('checker_type', models.CharField(default=b'N', max_length=1,
                                                  choices=[(b'N', b'NONE'), (b'4', b'404'), (b'X', b'404_OR_X_PATH')])),
                ('checker_x_path', models.CharField(max_length=200, blank=True)),
                ('checker_x_path_result', models.CharField(max_length=200, blank=True)),
                ('checker_ref_url', models.URLField(max_length=500, blank=True)),
                ('comments', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('pipelines', models.ManyToManyField(to='scraper.Pipelines', blank=True)),
                ('scraped_obj_class', models.ForeignKey(to='scraper.ScrapedObjClass')),
            ],
            options={
                'ordering': ['name', 'scraped_obj_class'],
                'verbose_name': '\u91c7\u96c6\u5668',
                'verbose_name_plural': '\u91c7\u96c6\u5668',
            },
        ),
        migrations.CreateModel(
            name='ScraperElem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x_path', models.CharField(max_length=200)),
                ('reg_exp', models.CharField(max_length=200, blank=True)),
                ('from_detail_page', models.BooleanField(default=False)),
                ('processors', models.CharField(max_length=200, blank=True)),
                ('proc_ctxt', models.TextField(blank=True)),
                ('mandatory', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('scraped_obj_attr', models.ForeignKey(to='scraper.ScrapedObjAttr')),
                ('scraper', models.ForeignKey(to='scraper.Scraper')),
            ],
            options={
                'verbose_name': '\u89c4\u5219',
                'verbose_name_plural': '\u89c4\u5219',
            },
        ),
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0')),
                ('domain', models.CharField(unique=True, max_length=100, verbose_name='\u57df\u540d', db_index=True)),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='\u522b\u540d')),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('category', models.ForeignKey(verbose_name='\u5206\u7c7b', to='scraper.Category')),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': '\u7ad9\u70b9',
                'verbose_name_plural': '\u7ad9\u70b9',
            },
        ),
        migrations.CreateModel(
            name='UserWebsite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u81ea\u5b9a\u4e49\u7c7b\u578b',
                'verbose_name_plural': '\u81ea\u5b9a\u4e49\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0')),
                ('url', models.URLField(unique=True, verbose_name='\u5730\u5740', db_index=True)),
                ('allow_domain', models.CharField(max_length=200, verbose_name='\u5141\u8bb8\u57df\u540d')),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('comments', models.TextField(verbose_name='\u4ecb\u7ecd', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('pipelines', models.ManyToManyField(to='scraper.Pipelines', blank=True)),
                ('scraper',
                 models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='scraper.Scraper',
                                   null=True)),
                ('scraper_runtime', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True,
                                                      to='scraper.SchedulerRuntime', null=True)),
                ('site', models.ForeignKey(verbose_name='\u7ad9\u70b9', to='scraper.Sites')),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': '\u7f51\u5740',
                'verbose_name_plural': '\u7f51\u5740',
            },
        ),
        migrations.AddField(
            model_name='userwebsite',
            name='website',
            field=models.ForeignKey(to='scraper.Website'),
        ),
        migrations.AddField(
            model_name='scrapedobjattr',
            name='obj_class',
            field=models.ForeignKey(to='scraper.ScrapedObjClass'),
        ),
        migrations.AddField(
            model_name='logmarker',
            name='scraper',
            field=models.ForeignKey(blank=True, to='scraper.Scraper', null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='scraper',
            field=models.ForeignKey(blank=True, to='scraper.Scraper', null=True),
        ),
        migrations.AddField(
            model_name='generalmodel',
            name='checker_runtime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True,
                                    to='scraper.SchedulerRuntime', null=True),
        ),
        migrations.AddField(
            model_name='generalmodel',
            name='website',
            field=models.ForeignKey(to='scraper.Website'),
        ),
    ]
