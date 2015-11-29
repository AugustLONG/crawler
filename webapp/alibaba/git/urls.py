from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', "git.views.index", name='git_home'),
    url(r'^$', "git.views.detail", name='git_detail'),
]