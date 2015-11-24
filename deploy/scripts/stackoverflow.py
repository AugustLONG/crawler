import datetime
import time, pymongo
from elasticsearch import Elasticsearch
from django.utils.html import strip_tags

es = Elasticsearch([{'host': "127.0.0.1"}])
conn = pymongo.MongoClient("127.0.0.1", 27017)
stackoverflowdb = conn.stackoverflow

def save_es(items):
    index = "it"
    _type = "stackoverflow_questions"
    from elasticsearch.helpers import bulk
    es.indices.create(index=index, body={
        'settings': {
            'number_of_shards': 4,
            'number_of_replicas': 0,
        },
        "mappings": {
            _type: {
                "properties": {
                    'body': {
                        'type': 'string',
                        'analyzer': 'snowball'
                    },
                    'title': {
                        'type': 'string',
                        'analyzer': 'snowball'
                    },
                }
            }
        }
    },ignore=400)
    bulk_items=[]
    i=0
    for item in items:
        now = datetime.datetime.now() - datetime.timedelta(hours=8)
        body = {"@timestamp": now}
        _id = str(item["_id"])
        del item["_id"]
        body.update(item)
        if not es.exists(index=index, doc_type=_type, id=_id):
            es.index(index=index, doc_type=_type, body=body, ignore=400, timestamp=now, id=_id, request_timeout=30)
            i += 1
            print i
            # bulk_items.append({'_type': 'stackoverflow',
            #                    '_id': _id,
            #                    '_source': body,
            #                    })
            # if i == 10000:
            #     success, _ = bulk(es, bulk_items, index='it', raise_on_error=True, request_timeout=1800)
            #     print('Performed %d actions' % success)
            #     bulk_items = []
            #     i = 0
    # es.indices.refresh(index=index)


if __name__ == '__main__':
    # es.indices.delete("it",ignore=400)
    items = stackoverflowdb.question.find({},{"body_markdown":0})
    save_es(items)
