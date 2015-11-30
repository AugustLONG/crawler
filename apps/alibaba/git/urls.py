from django.conf.urls import patterns, url, include

urlpatterns = patterns('git.views',
    url(r'^$', "index", name='git_home'),
    url(r'^$', "detail", name='git_detail'),
    )