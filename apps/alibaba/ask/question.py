__author__ = 'lifeifei'
import time
from django.conf import settings
from django.shortcuts import render_to_response,RequestContext,Http404
from bson import ObjectId
from silk.profiling.profiler import silk_profile

mongodb = settings.MONGODB
es = settings.ES

def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


def detail(request, pk):
    stackoverflowdb = mongodb["stackoverflow"]
    question = stackoverflowdb["question"].find_one(ObjectId(pk))
    if not question:
        raise Http404
    answers = stackoverflowdb["answer"].find({"question_id": question["question_id"]})
    relate_questions=[]
    with silk_profile(name='Search By Keywords #%s' % question["title"]):
        datas = es.search(index='it', doc_type='stackoverflow_questions', body={
            "query": {
                "filtered": {
                    "query": {
                        "match": {
                            "title": {
                                "query": question["title"].lower(),
                                "minimum_should_match": "30%",
                                "operator": "or"
                            }
                        }
                    }
                }
            },
            "from": 0,
            "size": 10,
            'sort': [
                {'_score': {'order': 'desc'}}
            ],
        })
        hits, took = datas["hits"], datas["took"]
        total = hits["total"]
        for h in hits["hits"]:
            relate_questions.append({
                "id": h["_id"],
                "body": h["_source"]["body"],
                "title": h["_source"]["title"],
                "tags": h["_source"]["tags"],
                "created": time.strftime('%Y-%m-%d',  time.localtime(h["_source"]["creation_date"]))
            })
    return render_to_response('ask/question/detail.html', {
        "question": question,
        "answers": answers,
        "relate_questions": relate_questions
    }, RequestContext(request))
