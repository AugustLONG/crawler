import datetime
import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pymongo

MONGO_HOST = "192.168.234.139"
MONGO_PORT = 27017
conn = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = conn.crawler
collection = db["nuomi"]

# by default we connect to localhost:9200
es = Elasticsearch([{'host': MONGO_HOST}])  # sniff_on_start=True, sniff_on_connection_fail=True,sniffer_timeout=60
# create an index in elasticsearch, ignore status code 400 (index already exists)
# es.indices.create(index='tuangou', ignore=400)
# es.indices.put_settings({
#                             "index": {
#                                 "number_of_replicas": 0,
#                                 "refresh_interval": "20s"
#                             }
#                         }, index="*")
# datetimes will be serialized

items = collection.find()
bulk_items = []
i = 0
for item in items:
    now = datetime.datetime.now() - datetime.timedelta(hours=8)
    body = {"@timestamp": now}
    _id = str(item["_id"])
    del item["_id"]
    body.update(item)
    # es.index(index="tuangou", doc_type="meituan", body=body, ignore=400, timestamp=now,refresh=3, id=_id,request_timeout=30)
    i += 1
    bulk_items.append({'_type': 'nuomi',
                       '_id': _id,
                       '_source': body,
                       })
    if i == 10000:
        success, _ = bulk(es, bulk_items, index='tuangou', raise_on_error=True, request_timeout=1800)
        print('Performed %d actions' % success)
        bulk_items = []
        i = 0
        time.sleep(10)
    # but not deserialized
    # es.get(index="my-index", doc_type="test-type", id=42)['_source']
    # {u'any': u'data', u'timestamp': u'2013-05-12T19:45:31.804229'}
