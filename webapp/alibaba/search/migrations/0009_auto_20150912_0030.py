# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_remove_pagemodule_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagemodule',
            name='page_type',
            field=models.CharField(default=b'L', max_length=1, choices=[(b'L', b'LIST'), (b'D', b'DETAIL'), (b'I', b'INDEX')]),
        ),
        migrations.AlterField(
            model_name='pagemodule',
            name='filter',
            field=models.TextField(help_text='\u5730\u533a\u3001\u5206\u7c7b\u3001tag\u3001\u7f51\u7ad9\u7b49\u7ec4\u5408\u67e5\u8be2\u6216\u8005\u663e\u793a', verbose_name='\u67e5\u8be2\u548c\u663e\u793a\u6761\u4ef6'),
        ),
    ]
