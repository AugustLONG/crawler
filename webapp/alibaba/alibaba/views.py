# coding=utf-8
from django.views.generic.base import TemplateView, View
from search.models import Category, Link, Tag
from django.core.cache import cache
import json
from django.conf import settings
from dateutil.parser import parse as parse_date
from silk.profiling.profiler import silk_profile
es = settings.ES
from elasticsearch_dsl import Search, Q

class HomePageView(TemplateView):
    template_name = "index.html"
    category_key = "all_category_list"
    category_key_ttl = 3600

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        categories = cache.get(self.category_key, [])
        if  not categories:
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

        print categories
        context['categories'] = categories

        links = Link.objects.all()
        context['links'] = links

        tags = Tag.objects.hot()[:10]
        context['tags'] = tags

        search = Search(using=es, index="tuangou", doc_type="meituan").sort('-@timestamp')[0:50]
        context["results"] = search.execute()
        return context

@silk_profile(name='View Blog Post')
def post(request, post_id):
    p = Post.objects.get(pk=post_id)
    return render_to_response('post.html', {
        'post': p
    })

class MyView(View):
    @silk_profile(name='View Blog Post')
    def get(self, request):
        p = Post.objects.get(pk=post_id)
        return render_to_response('post.html', {
            'post': p
        })

def post(request, post_id):
    with silk_profile(name='View Blog Post #%d' % self.pk):
        p = Post.objects.get(pk=post_id)
        return render_to_response('post.html', {
            'post': p
        })