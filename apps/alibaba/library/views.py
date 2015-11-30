from django.conf import settings
from django.shortcuts import render_to_response,RequestContext

def index(request):
    return render_to_response('index.html', {}, RequestContext(request))

def detail(request):
    return render_to_response('detail.html', {}, RequestContext(request))