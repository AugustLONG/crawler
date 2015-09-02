#!/usr/bin/env python
# coding=utf-8

from elasticsearch import Elasticsearch

PAGE_SIZE = 10


def do_search(query, page):
    es = Elasticsearch(['115.28.168.184:9200'], timeout=5)

    page = int(page)
    if page < 1:
        page = 1

    search_res = es.search(index='zhidao', doc_type='ZDQuestionItem', body={
    "query": {
        "filtered": {
            "query": {
                "match": {
                    "ask_title": query
                }
            }
        }
    },
    "from": page,
    "size": 10,
    "highlight": {
        "fields": {
            "ask_title": {},
            "content": {},
            "answers": {}
        }
    }
})
    results = search_res["hits"]
    return results