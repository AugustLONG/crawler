from django.shortcuts import render_to_response,RequestContext


def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


def detail(request, pk):
    return render_to_response('ask/detail.html', {}, RequestContext(request))
