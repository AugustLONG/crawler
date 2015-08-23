# coding=utf-8
from django.views.generic.base import TemplateView
from search.models import Category, Link, Tag
from django.core.cache import cache
import json
from elasticsearch import Elasticsearch
from django.conf import settings
from dateutil.parser import parse as parse_date


class HomePageView(TemplateView):
    template_name = "index.html"
    category_key = "all_category_list"
    category_key_ttl = 3600

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        categories = cache.get(self.category_key, [])
        if not categories:
            for category in Category.objects.roots():
                categories_dict = {"name": category.name, "url": category.get_absolute_url(), "children": [], "hot": []}
                for children in Category.objects.chriden(category.pk):
                    children_dict = {"name": children.name, "url": children.get_absolute_url(), "children": []}
                    for child in Category.objects.chriden(children.pk):
                        child_dict = {"name": child.name, "url": child.get_absolute_url()}
                        children_dict["children"].append(child_dict)
                        if child.hot >= 10:
                            categories_dict["hot"].append(child_dict)
                    categories_dict["children"].append(children_dict)
                categories.append(categories_dict)
            cache.set(self.category_key, json.dumps(categories), self.category_key_ttl)
        else:
            categories = json.loads(categories)
        context['categories'] = categories

        links = Link.objects.all()
        context['links'] = links

        tags = Tag.objects.hot()[:10]
        context['tags'] = tags

        es = Elasticsearch(settings.ES_HOST)
        results = es.search(
            index="tuangou",
            doc_type="nuomi",
            body={
                "size": 50,
                "sort": [
                    {
                        "@timestamp": {
                            "order": "desc",
                            "ignore_unmapped": True
                        }
                    }
                ]
            })
        datas =[]
        for result in results['hits']['hits']:
            datas.append(result["_source"])
        context["results"]=datas
        return context