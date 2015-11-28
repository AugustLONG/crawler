from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', "ask.views.index", name='ask_home'),
]