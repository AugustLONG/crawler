# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import easy_thumbnails.fields

import userena.models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mugshot',
                 easy_thumbnails.fields.ThumbnailerImageField(help_text='A personal image displayed in your profile.',
                                                              upload_to=userena.models.upload_to_mugshot,
                                                              verbose_name='mugshot', blank=True)),
                ('privacy', models.CharField(default=b'registered', help_text='Designates who can view your profile.',
                                             max_length=15, verbose_name='privacy',
                                             choices=[(b'open', 'Open'), (b'registered', 'Registered'),
                                                      (b'closed', 'Closed')])),
                ('language',
                 models.CharField(default=b'zh', help_text='Default language.', max_length=5, verbose_name='language',
                                  choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'),
                                           (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'),
                                           (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'),
                                           (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'),
                                           (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'),
                                           (b'en', b'English'), (b'en-au', b'Australian English'),
                                           (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'),
                                           (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'),
                                           (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'),
                                           (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'),
                                           (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'),
                                           (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'),
                                           (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'),
                                           (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'),
                                           (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'),
                                           (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'),
                                           (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'),
                                           (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'),
                                           (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'),
                                           (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'),
                                           (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'),
                                           (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'),
                                           (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'),
                                           (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'),
                                           (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'),
                                           (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'),
                                           (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'),
                                           (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'),
                                           (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'),
                                           (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'),
                                           (b'zh-tw', b'Traditional Chinese')])),
                ('gender', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='gender',
                                                            choices=[(1, 'Male'), (2, 'Female')])),
                ('website', models.URLField(verbose_name='website', blank=True)),
                ('location', models.CharField(max_length=255, verbose_name='location', blank=True)),
                ('birth_date', models.DateField(null=True, verbose_name='birth date', blank=True)),
                ('about_me', models.TextField(verbose_name='about me', blank=True)),
                (
                    'user',
                    models.OneToOneField(related_name='profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'permissions': (('view_profile', 'Can view profile'),),
            },
        ),
    ]
