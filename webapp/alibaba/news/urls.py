from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', "news.views.index", name='news_home'),
    url(r'^$', "news.views.detail", name='news_detail'),
]