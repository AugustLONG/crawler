from django.conf.urls import patterns, url, include

urlpatterns = patterns('ask.views',
    url(r'^$', "index", name='ask_home'),
    url(r'^(?P<pk>[0-9A-Za-z]+).html$', "detail", name='ask_detail'),
)

urlpatterns += patterns('ask.question',
    url(r'^$', "index", name='ask_question_home'),
    url(r'^question/(?P<pk>[0-9A-Za-z]+).html$', "detail", name='ask_question_detail'),
)