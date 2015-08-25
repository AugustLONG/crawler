#coding=utf-8
"""crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf import settings
from alibaba.views import HomePageView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from accounts.forms import SignupFormExtra, AuthenticationFormExtra
admin.autodiscover()


urlpatterns = [
    url(r'^wanglingling/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^category/(?P<slug>\w+)$', HomePageView.as_view(), name='search_by_category'),
    url(r'^messages/', include('userena.contrib.umessages.urls')),
    url(r'^accounts/signup/$','userena.views.signup',{'signup_form': SignupFormExtra}),
    url(r'^accounts/signin/$','userena.views.signin',{'auth_form': AuthenticationFormExtra}),
    url(r'^accounts/', include('userena.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^captcha/', include('captcha.urls')),


]

urlpatterns += patterns('', url(r'^silk/', include('silk.urls', namespace='silk')))

urlpatterns += patterns('', url(r'', include('social_auth.urls')))

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
