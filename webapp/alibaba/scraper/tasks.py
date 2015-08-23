#coding=utf-8
"""
celery异步任务调度
"""
from celery.task import task

from crawler.utils.task_utils import TaskUtils
from scraper.models import Scraper, Website

@task()
def run_spiders():
    t = TaskUtils()
    t.run_spiders(Website, 'scraper', 'scraper_runtime', 'article_spider')

@task()
def run_checkers():
    t = TaskUtils()
    t.run_checkers(Scraper, 'news_website__scraper', 'checker_runtime', 'article_checker')