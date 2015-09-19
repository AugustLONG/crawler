#coding=utf-8
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from search.models import Category
from django.shortcuts import render_to_response,Http404
from django.template.context import RequestContext
from scraper.models import Website
from search.models import PageModule,Topic
from braces.views import LoginRequiredMixin


def search_result(request, website_slug):
    p = Website.objects.get(pk=website_slug)
    q = request.GET.get("q")
    return render_to_response('search/result.html', {'q': q})


def search_detail(request, website_slug, category_slug, pk):
    """
    结果的详情页面
    """
    p = Website.objects.get(pk=pk)
    result = None
    return render_to_response('search/detail.html', {'result': result})


def topic_list(request, website_slug=None):
    """
    专题列表
    :param request:
    :param post_id:
    :return:
    """
    topics = Topic.objects.filter(enabled=True)
    return render_to_response('topic/list.html', {'topics': topics})


def topic_detail(request, post_id):
    """
    专题详情页面
    :param request:
    :param post_id:
    :return:
    """
    try:
        topic = Topic.objects.get(pk=post_id, enabled=True)
    except:
        raise Http404
    return render_to_response('topic/detail.html', {'topic': topic})