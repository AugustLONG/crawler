from django.conf.urls import *

urlpatterns = patterns('search.views',
                       url(r'^list_(?P<kd>[^\?]+)$', 'search_list', name='alibaba_search_list'),
                       url(r'^/(?P<website_slug>\w+)_(?P<pk>\w+).html$', 'search_detail', name='alibaba_search_detail'),

                       )
