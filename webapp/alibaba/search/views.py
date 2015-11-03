# coding=utf-8
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, Http404, render
from django.template.context import RequestContext
from scraper.models import Website
from search.models import PageModule, Topic
from braces.views import LoginRequiredMixin
from django.conf import settings
from elasticsearch_dsl import Search, Q
from bson.objectid import ObjectId
import traceback


PER_COUNT = 50
PAGE_MAC_SIZE = 20
BEFORE_RANGE_NUM = AFTER_RANGE_NUM = 10

es = settings.ES


def search_list(request, kd=None):
    kd = request.GET.get("kd", None)
    if not kd:
        raise Http404
    else:
        kd = kd.strip()
    page = int(request.GET.get("page", "1"))
    if page > PAGE_MAC_SIZE:
        page = PAGE_MAC_SIZE
    elif page < 1:
        page = 1
    spc = request.GET.get("spc", "1")
    city = request.GET.get("city", u"全国")
    pn_count = (page - 1) * PER_COUNT
    tags = {"cities": [], "websites": []}
    page_size=1
    try:
        search = Search(using=es, index="tuangou", doc_type="meituan").query("match", title=kd).sort('-@timestamp')[
                 pn_count:pn_count + PER_COUNT]
        # s..query(~Q("match", description="beta"))  # description字段不含 beta
        search.aggs.bucket('per_city', 'terms', field='city')  # metric('max_lines', 'max', field='lines')
        search.aggs.bucket('per_website', 'terms', field='website')
        page_size = search.count() / PER_COUNT + 1
        response = search.execute()
        # print search.count()


        # for hit in response:
        #     print dir(hit.meta) # ['doc_type', u'id', u'index', u'score', u'sort']
        #     print dir(hit)

        for tag in response.aggregations.per_city.buckets:
            # print tag.key, tag.doc_count
            tags["cities"].append((tag.key, tag.doc_count))
            # print(tag.key, tag.sum_lines.value)
        for tag in response.aggregations.per_website.buckets:
            # print tag.key, tag.doc_count
            tags["websites"].append((tag.key, tag.doc_count))
    except:
        exception=traceback.format_exc()
        print exception
    host_search = [u"美食", u"酒店", u"机票", u"火车票", u"汽车票"]
    if page_size > PAGE_MAC_SIZE:
        page_size = PAGE_MAC_SIZE
    ct = dict({
        'kd': kd,
        'results': response,
        "spc": spc,
        "city": city,
        "page": page,
        "page_size": page_size,
        "host_search": host_search,

    })
    return render(request, 'search/list.html', ct)


def search_detail(request, website_slug, pk):
    """
    结果的详情页面
    """
    search = Search(using=es, index="tuangou", doc_type="meituan").query("match", _id=pk)
    result = search.execute()[0]
    print result
    return render(request, 'search/detail.html', {'result': result})


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
