# encoding: utf-8
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request
import re, json,time
from pymongo import MongoClient

mongodb = MongoClient()
stackoverflowdb = mongodb.stackoverflow
key="&key=U4DMV*8nvpm3EOpvf69Rxw(("

class StackoverflowSpider(CrawlSpider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com", "stackexchange.com"]
    # start_urls = [
    #
    # ]

    def start_requests(self):
        for i in range(2,500):
            i=str(i)
            yield Request('http://api.stackexchange.com/2.2/questions?page='+i+'&pagesize=50&order=desc&sort=activity&site=stackoverflow&filter=!9YdnSQHvY'+key,
                                 self.parse_questions)
            yield Request('http://api.stackexchange.com/2.2/answers?page='+i+'&pagesize=50&order=desc&sort=activity&site=stackoverflow&filter=!)rCcH8tl1NCISRRturSV'+key,
                                 self.parse_answers)
            yield Request('http://api.stackexchange.com/2.2/users?page='+i+'&pagesize=50&order=desc&sort=reputation&site=stackoverflow&filter=!9YdnSQHvY'+key,
                                 self.parse_users)
            yield Request('http://api.stackexchange.com/2.2/comments?page='+i+'&pagesize=50&order=desc&sort=creation&site=stackoverflow&filter=!b0OfN.wWgRBMab'+key,
                                 self.parse_comments)

    def delay(self,seconds=10):
        time.sleep(seconds)

    def parse_users(self, response):
        self.delay()
        items = json.loads(response.body)
        if "items" in items:
            for item in items["items"]:
                user_id = item["user_id"]
                stackoverflowdb.user.update({"user_id": user_id}, {"$set": item}, upsert=True)
                if "answers" in item:
                    for answer in item["answers"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/answers/%s?order=desc&sort=activity&site=stackoverflow&filter=!LUcFBIwXAv-E7rc11-bLO." %
                            answer["answer_id"]+key, callback=self.parse_answers)
                    del item["answers"]
                if "comments" in item:
                    for comment in item["comments"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/comments/%s?order=desc&sort=creation&site=stackoverflow&filter=!b0OfN.wWgRBMab" %
                            comment["comment_id"]+key, callback=self.parse_comments)
                    del item["comments"]
                if "questions" in item:
                    for question in item["questions"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/questions/%s?order=desc&sort=activity&site=stackoverflow&filter=!0Uv6ZT)teRUpIDUXg)eKBUB)K" %
                            question["question_id"]+key, callback=self.parse_questions)
                    del item["questions"]

    def parse_questions(self, response):
        self.delay()
        items = json.loads(response.body)
        if "items" in items:
            for item in items["items"]:
                owner_id = item["owner"]["user_id"]
                item["owner_id"] = owner_id
                question_id = item["question_id"]
                del item["owner"]
                stackoverflowdb.question.update({"question_id": question_id}, {"$set": item}, upsert=True)
                yield Request(
                    "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % owner_id+key,
                    callback=self.parse_users)
                if "answers" in item:
                    for answer in item["answers"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/answers/%s?order=desc&sort=activity&site=stackoverflow&filter=!LUcFBIwXAv-E7rc11-bLO." %
                            answer["answer_id"]+key, callback=self.parse_answers)
                    del item["answers"]
                if "comments" in item:
                    for comment in item["comments"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/comments/%s?order=desc&sort=creation&site=stackoverflow&filter=!b0OfN.wWgRBMab" %
                            comment["comment_id"]+key, callback=self.parse_comments)
                    del item["comments"]

    def parse_answers(self, response):
        self.delay()
        items = json.loads(response.body)
        if "items" in items:
            for item in items["items"]:
                owner_id = item["owner"]["user_id"]
                item["owner_id"] = owner_id
                answer_id = item["answer_id"]
                stackoverflowdb.answer.update({"answer_id": answer_id}, {"$set": item}, upsert=True)
                yield Request(
                    "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % owner_id+key,
                    callback=self.parse_users)

    def parse_comments(self, response):
        self.delay()
        items = json.loads(response.body)
        if "items" in items:
            for item in items["items"]:
                owner_id = item["owner"]["user_id"]
                item["owner_id"] = owner_id
                if "reply_to_user" in item:
                    reply_to_user_id = item["reply_to_user"]["user_id"]
                    item["reply_to_user_id"] = reply_to_user_id
                    del item["reply_to_user"]
                comment_id = item["comment_id"]
                del item["owner"]
                stackoverflowdb.comment.update({"comment_id": comment_id}, {"$set": item}, upsert=True)
                yield Request(
                    "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % owner_id+key,
                    callback=self.parse_users)
                if "reply_to_user" in item:
                    yield Request(
                        "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % reply_to_user_id+key,
                        callback=self.parse_users)