# encoding: utf-8
from __future__ import unicode_literals

from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    captcha = CaptchaField()
