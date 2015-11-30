from django.conf.urls import patterns, url, include

urlpatterns = patterns('news.views',
    url(r'^$', "index", name='news_home'),
    url(r'^$', "detail", name='news_detail'),
    )