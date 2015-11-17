# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='City',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0', blank=True)),
				('chart', models.CharField(max_length=200, verbose_name='url\u6807\u5fd7', blank=True)),
				('ename', models.CharField(max_length=200, verbose_name='\u82f1\u6587\u7b80\u79f0', blank=True)),
				('code', models.CharField(max_length=200, verbose_name='\u7f16\u7801', blank=True)),
				('airport', models.CharField(max_length=200, verbose_name='\u822a\u7a7a', blank=True)),
				('status', models.BooleanField(default=False, verbose_name='\u542f\u7528')),
				('latitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7ecf\u5ea6')),
				('longitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7eac\u5ea6')),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
			],
			options={
				'ordering': ('name',),
				'verbose_name': '\u57ce\u5e02',
				'verbose_name_plural': '\u57ce\u5e02',
			},
		),
		migrations.CreateModel(
			name='Country',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0', blank=True)),
				('chart', models.CharField(max_length=200, verbose_name='url\u6807\u5fd7', blank=True)),
				('ename', models.CharField(max_length=200, verbose_name='\u82f1\u6587\u7b80\u79f0', blank=True)),
				('status', models.BooleanField(default=False, verbose_name='\u542f\u7528')),
				('latitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7ecf\u5ea6')),
				('longitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7eac\u5ea6')),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
			],
			options={
				'ordering': ('name',),
				'verbose_name': '\u56fd\u5bb6',
				'verbose_name_plural': '\u56fd\u5bb6',
			},
		),
		migrations.CreateModel(
			name='Location',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0', blank=True)),
				('chart', models.CharField(max_length=200, null=True, verbose_name='url\u6807\u5fd7', blank=True)),
				('ename',
				 models.CharField(max_length=200, null=True, verbose_name='\u82f1\u6587\u7b80\u79f0', blank=True)),
				('status', models.BooleanField(default=False, verbose_name='\u542f\u7528')),
				('latitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7ecf\u5ea6')),
				('longitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7eac\u5ea6')),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
				('city', models.ForeignKey(to='alibaba.City')),
			],
			options={
				'ordering': ('name',),
				'verbose_name': '\u884c\u653f\u533a',
				'verbose_name_plural': '\u884c\u653f\u533a',
			},
		),
		migrations.CreateModel(
			name='Province',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0', blank=True)),
				('chart', models.CharField(max_length=200, verbose_name='url\u6807\u5fd7', blank=True)),
				('ename', models.CharField(max_length=200, verbose_name='\u82f1\u6587\u7b80\u79f0', blank=True)),
				('status', models.BooleanField(default=False, verbose_name='\u542f\u7528')),
				('latitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7ecf\u5ea6')),
				('longitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7eac\u5ea6')),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
				('country', models.ForeignKey(to='alibaba.Country')),
			],
			options={
				'ordering': ('name',),
				'verbose_name': '\u7701\u4efd',
				'verbose_name_plural': '\u7701\u4efd',
			},
		),
		migrations.CreateModel(
			name='Zone',
			fields=[
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
				('name', models.CharField(max_length=200, verbose_name='\u540d\u79f0')),
				('chart', models.CharField(max_length=200, null=True, verbose_name='url\u6807\u5fd7', blank=True)),
				('ename',
				 models.CharField(max_length=200, null=True, verbose_name='\u82f1\u6587\u7b80\u79f0', blank=True)),
				('status', models.BooleanField(default=False, verbose_name='\u542f\u7528')),
				('latitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7ecf\u5ea6')),
				('longitude', models.FloatField(default=0.0, max_length=100, verbose_name='\u7eac\u5ea6')),
				('desc', models.TextField(verbose_name='\u7b80\u4ecb', blank=True)),
				('mapuse', models.CharField(max_length=2, verbose_name='\u5730\u56fe\u4f7f\u7528')),
				('mappic',
				 models.CharField(max_length=40, null=True, verbose_name='\u5730\u56fe\u56fe\u7247', blank=True)),
				('range', models.CharField(max_length=100, null=True, verbose_name='Range', blank=True)),
				('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
				('updated', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
				('city', models.ForeignKey(verbose_name='\u57ce\u5e02', to='alibaba.City')),
			],
			options={
				'ordering': ('name',),
				'verbose_name': '\u5546\u4e1a\u533a',
				'verbose_name_plural': '\u5546\u4e1a\u533a',
			},
		),
		migrations.AddField(
			model_name='city',
			name='country',
			field=models.ForeignKey(to='alibaba.Country'),
		),
		migrations.AddField(
			model_name='city',
			name='province',
			field=models.ForeignKey(to='alibaba.Province'),
		),
	]
