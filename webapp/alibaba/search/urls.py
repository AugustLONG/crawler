from django.conf.urls import *
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('search.views',
    url(r'^list_(?P<kd>[^\?]+)$', 'search_list', name='alibaba_search_list'),

)
