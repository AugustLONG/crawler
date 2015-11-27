# coding=utf-8
import json

from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render_to_response, RequestContext
from django.template.defaultfilters import strip_tags, mark_safe
from dateutil.parser import parse as parse_date
from silk.profiling.profiler import silk_profile

es = settings.ES
PAGE_SIZE=50
PAGE_COUNTER=10

def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


@silk_profile(name='Search By Keywords')
def search(request):
    keywords = request.GET.get("keywords", None)
    page = int(request.GET.get("page", 1))
    if page < 1:
        page = 1
    elif page>PAGE_COUNTER:
        page=PAGE_COUNTER
    if keywords and keywords.strip():
        keywords = strip_tags(keywords.strip())
        with silk_profile(name='Search By Keywords #%s' % keywords):
            datas = es.search(index='it', doc_type='stackoverflow_questions', body={
                "query": {
                    "filtered": {
                        "query": {
                            "match": {
                                "title": keywords.lower()
                            }
                        }
                    }
                },
                "from": (page-1)*PAGE_SIZE,
                "size": PAGE_SIZE,
                "highlight": {
                    "fields": {
                        "light_title": {

                        },
                    }
                }
            })
            hits, took = datas["hits"], datas["took"]
            total = hits["total"]
            results = []
            for h in hits["hits"]:
                results.append({
                    "body": h["_source"]["body"],
                    "title": h["_source"]["title"]
                })
    else:
        results = []
        total = 0
    total_page = total / PAGE_SIZE
    if total_page < PAGE_COUNTER:
        page_list = range(1, total_page)
    elif page + PAGE_COUNTER < total_page:
        page_list = range(1, page + PAGE_COUNTER)
    else:
        page_list = range(1, total_page)
    if len(page_list)>PAGE_COUNTER:
        page_list=page_list[:PAGE_COUNTER]
    next_page = 0 if int(page) + 1 >= total_page else page + 1
    return render_to_response('list.html', {"results": results,
                                            "total": total,
                                            "page": page,
                                            "keywords": keywords,
                                            "page_list":page_list,
                                            "next_page":next_page
                                            },
                              RequestContext(request))


@silk_profile(name='Search By Keywords')
def detail(request, slug, pk):
    results = []
    return render_to_response('detail.html', {"results": results}, RequestContext(request))

#
#
# def post(request, post_id):
#     with silk_profile(name='View Blog Post #%d' % self.pk):
#         p = Post.objects.get(pk=post_id)
#         return render_to_response('post.html', {
#             'post': p
#         })
