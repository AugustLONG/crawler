# coding=utf-8
import json

from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render_to_response,RequestContext
from django.template.defaultfilters import strip_tags,mark_safe
from dateutil.parser import parse as parse_date
from silk.profiling.profiler import silk_profile
es = settings.ES


def index(request):
    return render_to_response('index.html', {},RequestContext(request))

@silk_profile(name='Search By Keywords')
def search(request):
    keywords=request.GET.get("keywords", None)
    if keywords and keywords.strip():
        keywords=strip_tags(keywords.strip())
        with silk_profile(name='Search By Keywords #%s' % keywords):
            page=request.GET.get("page", 1)
            datas=es.search(index='it', doc_type='stackoverflow_questions', body={
                "query": {
                    "filtered": {
                        "query": {
                            "match": {
                                "title": keywords.lower()
                            }
                        }
                    }
                },
                "from": page,
                "size": 50,
                "highlight": {
                    "fields": {
                        "light_title": {

                        },
                    }
                }
            })
            print datas
            hits, took = datas["hits"], datas["took"]
            total=hits["total"]
            results=[]
            for h in hits["hits"]:
                results.append({
                    "body":h["_source"]["body"],
                    "title":h["_source"]["title"]
                })
    else:
        results = {"hits":{"hits":[]}}
        total=0
    return render_to_response('list.html', {"results": results, "total": total,"keywords":keywords},RequestContext(request))


@silk_profile(name='Search By Keywords')
def detail(request,slug,pk):
    results=[]
    return render_to_response('detail.html', {"results":results},RequestContext(request))
#
#
# def post(request, post_id):
#     with silk_profile(name='View Blog Post #%d' % self.pk):
#         p = Post.objects.get(pk=post_id)
#         return render_to_response('post.html', {
#             'post': p
#         })
