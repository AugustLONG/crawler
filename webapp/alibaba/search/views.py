#coding=utf-8
from django.shortcuts import render
from django.views.generic.base import TemplateView
from search.models import Category

class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context