#!/usr/bin/env python
# coding=utf-8

from django.conf import settings
from elasticsearch import Elasticsearch

PAGE_SIZE = 10


class ES:
    def __init__(self):
        self.es = settings.ES

    def search(self, index):
        s = Search(using=self.es, index=index) \
            .filter("term", category="search") \
            .query("match", title="python") \
            .query(~Q("match", description="beta"))

        s.aggs.bucket('per_tag', 'terms', field='tags') \
            .metric('max_lines', 'max', field='lines')
        response = s.execute()
        for hit in response:
            print(hit.meta.score, hit.title)

        for tag in response.aggregations.per_tag.buckets:
            print(tag.key, tag.max_lines.value)



    def page_search(self, query, page):

        page = int(page)
        if page < 1:
            page = 1

        search_res = self.es.search(index='zhidao', doc_type='ZDQuestionItem', body={
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
