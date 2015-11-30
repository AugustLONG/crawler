from django.conf.urls import patterns, url, include

urlpatterns = patterns('code.views',
    url(r'^$', "index", name='code_home'),
    url(r'^$', "detail", name='code_detail'),
)