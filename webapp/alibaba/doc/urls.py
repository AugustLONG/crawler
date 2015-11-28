from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', "doc.views.index", name='doc_home'),
]