# -*- coding: utf-8 -*-
import sys
import os
from xml.dom import minidom

import pymongo

crawler = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if sys.path.count(crawler) == 0:
    sys.path.insert(0, crawler)
reload(sys)
sys.setdefaultencoding('utf-8')


def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''


def get_nodevalue(node, index=0):
    return node.childNodes[index].nodeValue if node else ''


def get_xmlnode(node, name):
    return node.getElementsByTagName(name) if node else []


if __name__ == "__main__":
    from crawler.settings import MONGO_HOST

    conn = pymongo.MongoClient(MONGO_HOST, 27017)
    db = conn.crawler
    meituandb = db.meituan
    # db.meituan.ensure_index('url', unique=False)
    # i = 0
    # for item in meituandb.find({}, ["id", "url", "_id"]):
    #     i += 1
    #     print i
    #     if meituandb.find({"url": item["url"]}).count() > 1:
    #         meituandb.remove({"_id": item["_id"]})
    #     id1 = item["id"]
    #     id1 = id1.split("/")[-1]
    #     meituandb.update({"_id": item["_id"]}, {"$set": {"id": id1}})
    # db.meituan.ensure_index('url', unique=True)
    # raise
    f = open("/Users/lifeifei/Downloads/dailydealgz-1", "r+")
    content = "<?xml version='1.0' encoding='UTF-8' ?>"
    for line in f:
        line = line.strip()

        if not line.startswith("<?xml") and not line.startswith("<urlset"):
            content += line
        if line == "</url>":
            dom = minidom.parseString(content)
            root = dom.documentElement
            url = get_xmlnode(root, 'loc')[0].childNodes[0].nodeValue
            item = {"site": "nuomi", "shops": [], "url": url, "apiType": "hao123"}
            display_nodes = get_xmlnode(root, 'display')[0].childNodes
            for display in display_nodes:
                if display.nodeName == "#text":
                    continue
                elif display.nodeName == "shops":
                    shop_nodes = get_xmlnode(display, 'shop')
                    shop = {}
                    for shop_node in shop_nodes:
                        for node in shop_node.childNodes:
                            if node.nodeName == "#text":
                                continue
                            elif node.childNodes:
                                shop[node.nodeName] = node.childNodes[0].nodeValue  # wholeText
                    item["shops"].append(shop)
                elif display.childNodes:
                    name = display.nodeName
                    item[name] = display.childNodes[0].nodeValue  # wholeText
                    if name == "identifier":
                        item["id"] = item[name]
                print item
                collection = db[item['site']]
                url = item['url']
                old_item = collection.find_one({"url": url}, ["url", "_id"])
                if old_item:
                    continue
                # item["_id"] = old_item["_id"]
                # collection.save(item)
                else:
                    collection.insert(item)
            content = "<?xml version='1.0' encoding='UTF-8' ?>"
        # print content
    f.close()
