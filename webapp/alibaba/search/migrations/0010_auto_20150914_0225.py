# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	dependencies = [
		('contenttypes', '0002_remove_content_type_name'),
		('search', '0009_auto_20150912_0030'),
	]

	operations = [
		migrations.CreateModel(
			name='CategoryForms',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('mustable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u5fc5\u987b')),
				('nullable', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7a7a')),
				('default_value', models.CharField(max_length=250, verbose_name='\u9ed8\u8ba4\u503c')),
				('htmlable', models.BooleanField(default=True, verbose_name='\u5141\u8bb8HTML')),
				('order', models.SmallIntegerField(default=0, verbose_name='\u6392\u5e8f')),
				('editable', models.BooleanField(default=False, verbose_name='\u662f\u5426\u53ef\u4ee5\u7f16\u8f91')),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
				('category', models.ForeignKey(blank=True, to='search.Category', null=True)),
			],
			options={
				'verbose_name': '\u5206\u7c7b\u8868\u5355',
				'verbose_name_plural': '\u5206\u7c7b\u8868\u5355',
			},
		),
		migrations.CreateModel(
			name='GeneralForms',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('name', models.CharField(max_length=200, verbose_name='\u7b80\u5355\u7684\u8bf4\u660e')),
				('cname', models.CharField(max_length=200, verbose_name='\u4e2d\u6587', blank=True)),
				('slug', models.CharField(max_length=200, verbose_name='\u522b\u540d', blank=True)),
				('ename', models.CharField(max_length=200, verbose_name='\u82f1\u6587', blank=True)),
				('jname', models.CharField(max_length=200, verbose_name='\u65e5\u6587', blank=True)),
				('kname', models.CharField(max_length=200, verbose_name='\u97e9\u6587', blank=True)),
				('rname', models.CharField(max_length=200, verbose_name='\u4fc4\u8bed', blank=True)),
				('object_id', models.PositiveIntegerField(verbose_name='\u5bf9\u8c61ID')),
				('form_type', models.CharField(max_length=10, verbose_name='\u8868\u5355\u7c7b\u578b',
				                               choices=[(b'select', b'SELECT'), (b'text', b'TEXT'),
				                                        (b'datetime', b'DATETIME'), (b'textarea', b'TEXTAREA'),
				                                        (b'date', b'DATE')])),
				('form_value',
				 models.CharField(help_text='\u5982\u679c\u662f\u8868\u5355\u7c7b\u578b\u662fselect,1:v,2:v2',
				                  max_length=250, verbose_name='\u8868\u5355\u503c\u57df', blank=True)),
				('form_attr', models.CharField(
					help_text='\u53ef\u4ee5\u662f\u957f\u5ea6\u9650\u5236\uff0c\u6837\u5f0f\u8c03\u6574\u7b49',
					max_length=250, verbose_name='\u8868\u5355\u5c5e\u6027', blank=True)),
				('max_length', models.PositiveIntegerField(default=200, verbose_name='\u6700\u5927\u957f\u5ea6')),
				('min_length', models.PositiveIntegerField(default=1, verbose_name='\u6700\u5c0f\u957f\u5ea6')),
				('value_type', models.CharField(default=b'char', max_length=10, verbose_name='\u503c\u7684\u7c7b\u578b',
				                                choices=[(b'char', b'char'), (b'email', b'email'),
				                                         (b'datetime', b'DATETIME'), (b'ip', b'IP'), (b'slug', b'SLUG'),
				                                         (b'int', b'int'), (b'date', b'DATE')])),
				('help_text', models.CharField(max_length=250, verbose_name='\u5e2e\u52a9')),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
				('content_type', models.ForeignKey(to='contenttypes.ContentType')),
			],
			options={
				'verbose_name': '\u57fa\u7840\u8868\u5355',
				'verbose_name_plural': '\u57fa\u7840\u8868\u5355',
			},
		),
		migrations.CreateModel(
			name='Topic',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0')),
				('title', models.CharField(max_length=200, verbose_name='\u9875\u9762\u6807\u9898')),
				('keywords', models.CharField(max_length=200, verbose_name='\u5173\u952e\u8bcd')),
				('description',
				 models.CharField(max_length=200, null=True, verbose_name='\u9875\u9762\u63cf\u8ff0', blank=True)),
				('slug', models.SlugField(verbose_name='\u522b\u540d')),
				('style', models.CharField(max_length=200, verbose_name='CSS\u6837\u5f0f\u5730\u5740')),
				('js', models.CharField(max_length=200, verbose_name='js\u5730\u5740')),
				('template', models.TextField(
					help_text='\u53ef\u4ee5\u662f\u6e32\u67d3\u52a8\u6001\u6216\u8005\u9759\u6001\u6a21\u677f',
					verbose_name='\u6a21\u677f', blank=True)),
				('url', models.CharField(
					help_text='\u5982\u679c\u6a21\u677f\u548c\u5730\u5740\u90fd\u5b58\u5728\uff0c\u5219\u5730\u5740\u662f\u72ec\u7acb\u7684\uff0c\u53ef\u4ee5\u76f4\u63a5\u8bbf\u95ee',
					max_length=200, verbose_name='\u6a21\u677f\u5730\u5740', blank=True)),
				('enabled', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
				('category', models.ForeignKey(blank=True, to='search.Category', null=True)),
			],
			options={
				'verbose_name': '\u4e13\u9898',
				'verbose_name_plural': '\u4e13\u9898',
			},
		),
		migrations.AlterModelOptions(
			name='pagemodule',
			options={'get_latest_by': 'created', 'verbose_name': '\u9875\u9762\u6a21\u5757',
			         'verbose_name_plural': '\u9875\u9762\u6a21\u5757'},
		),
		migrations.AddField(
			model_name='pagemodule',
			name='category',
			field=models.ForeignKey(blank=True, to='search.Category', null=True),
		),
		migrations.AddField(
			model_name='pagemodule',
			name='description',
			field=models.CharField(max_length=200, verbose_name='\u9875\u9762\u63cf\u8ff0', blank=True),
		),
		migrations.AddField(
			model_name='pagemodule',
			name='keywords',
			field=models.CharField(max_length=200, verbose_name='\u5173\u952e\u8bcd', blank=True),
		),
		migrations.AddField(
			model_name='pagemodule',
			name='title',
			field=models.CharField(max_length=200, verbose_name='\u9875\u9762\u6807\u9898', blank=True),
		),
		migrations.AlterField(
			model_name='pagemodule',
			name='name',
			field=models.CharField(max_length=200, verbose_name='\u540d\u79f0', blank=True),
		),
		migrations.AddField(
			model_name='categoryforms',
			name='forms',
			field=models.ForeignKey(to='search.GeneralForms'),
		),
	]
