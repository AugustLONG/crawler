# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generalmodel',
            name='checker_runtime',
        ),
        migrations.RemoveField(
            model_name='generalmodel',
            name='website',
        ),
        migrations.RemoveField(
            model_name='userwebsite',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userwebsite',
            name='website',
        ),
        migrations.AddField(
            model_name='scraper',
            name='page_url_script',
            field=models.TextField(verbose_name='\u5217\u8868\u9875\u6267\u884c\u811a\u672c', blank=True),
        ),
        migrations.AddField(
            model_name='website',
            name='category',
            field=models.ForeignKey(default=True, verbose_name='\u5206\u7c7b', blank=True, to='scraper.Category'),
        ),
        migrations.AlterField(
            model_name='scraper',
            name='content_type',
            field=models.CharField(default=b'H',
                                   help_text=b'Data type format for scraped main pages (for JSON use JSONPath instead of XPath)',
                                   max_length=1,
                                   choices=[(b'H', b'HTML'), (b'X', b'XML'), (b'J', b'JSON'), (b'S', b'SCRIPT')]),
        ),
        migrations.AlterField(
            model_name='scraper',
            name='detail_page_content_type',
            field=models.CharField(default=b'H',
                                   help_text=b'Data type format for detail pages and checker (for JSON use JSONPath instead of XPath)',
                                   max_length=1,
                                   choices=[(b'H', b'HTML'), (b'X', b'XML'), (b'J', b'JSON'), (b'S', b'SCRIPT')]),
        ),
        migrations.DeleteModel(
            name='GeneralModel',
        ),
        migrations.DeleteModel(
            name='UserWebsite',
        ),
    ]
