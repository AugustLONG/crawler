# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('scraper', '0002_auto_20150911_2314'),
        ('search', '0006_auto_20150823_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageModule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u9875\u9762\u540d\u79f0')),
                ('slug', models.SlugField(verbose_name='\u522b\u540d')),
                ('style', models.CharField(max_length=200, verbose_name='CSS\u6837\u5f0f\u5730\u5740')),
                ('js', models.CharField(max_length=200, verbose_name='js\u5730\u5740')),
                ('template', models.TextField(help_text='\u53ef\u4ee5\u662f\u5730\u5740\u6216\u8005\u5185\u5bb9',
                                              verbose_name='\u6a21\u677f')),
                ('filter', models.TextField(
                    help_text='\u5730\u533a\u3001\u5206\u7c7b\u3001tag\u3001\u7f51\u7ad9\u7b49\u7ec4\u5408\u67e5\u8be2',
                    verbose_name='\u67e5\u8be2\u6761\u4ef6')),
                ('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('scraper', models.ForeignKey(to='scraper.Scraper')),
                ('website', models.ForeignKey(to='scraper.Website')),
            ],
            options={
                'get_latest_by': 'created',
                'verbose_name': '\u53cb\u60c5\u8fde\u63a5',
                'verbose_name_plural': '\u53cb\u60c5\u8fde\u63a5',
            },
        ),
    ]
