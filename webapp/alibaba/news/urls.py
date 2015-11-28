from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', "news.views.index", name='news_home'),
]