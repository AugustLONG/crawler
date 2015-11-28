from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', "code.views.index", name='code_home'),
]