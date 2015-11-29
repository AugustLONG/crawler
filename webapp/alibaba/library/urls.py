from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', "library.views.index", name='library_home'),
    url(r'^$', "library.views.detail", name='library_detail'),
]