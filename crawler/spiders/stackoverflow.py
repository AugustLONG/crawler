# encoding: utf-8
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import Request
import re, json
from pymongo import MongoClient

mongodb = MongoClient()
stackoverflowdb = mongodb.stackoverflow


class StackoverflowSpider(CrawlSpider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com", "stackexchange.com"]
    start_urls = [
        "http://api.stackexchange.com/2.2/questions?page=1&pagesize=50&order=desc&sort=activity&site=stackoverflow&filter=!9YdnSQHvY",
        "http://api.stackexchange.com/2.2/answers?order=desc&sort=reputation&site=stackoverflow&filter=!9YdnSQHvY",
        "http://api.stackexchange.com/2.2/users?order=desc&sort=reputation&site=stackoverflow&filter=!9YdnSQHvY",
        "http://api.stackexchange.com/2.2/comments?order=desc&sort=reputation&site=stackoverflow&filter=!9YdnSQHvY"
    ]

    def parse(self, response):
        items = json.loads(response.content)
        if "items" in items:
            for item in items:
                owner_id = item["owner"]["user_id"]
                item["owner_id="] = owner_id
                question_id = item["question_id"]
                del item["owner"]
                stackoverflowdb.question.update({"question_id": question_id}, {"$set": item}, upsert=True)
                yield Request(
                    "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % owner_id,
                    callback=self.parse_users)
                yield Request(
                    "http://api.stackexchange.com/2.2/questions/%s?order=desc&sort=activity&site=stackoverflow&filter=!0Uv6ZT)teRUpIDUXg)eKBUB)K" % question_id,
                    callback=self.parse_questions)

    def parse_users(self, response):
        items = json.loads(response.content)
        if "items" in items:
            for item in items:
                user_id = item["user_id"]
                stackoverflowdb.user.update({"user_id": user_id}, {"$set": item}, upsert=True)
                if "answers" in item:
                    for answer in item["answers"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/answers/%s?order=desc&sort=activity&site=stackoverflow&filter=!LUcFBIwXAv-E7rc11-bLO." %
                            answer["answer_id"], callback=self.parse_answers)
                    del item["answers"]
                if "comments" in item:
                    for comment in item["comments"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/comments/%s?order=desc&sort=creation&site=stackoverflow&filter=!b0OfN.wWgRBMab" %
                            comment["comment_id"], callback=self.parse_comments)
                    del item["comments"]
                if "questions" in item:
                    for question in item["questions"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/questions/%s?order=desc&sort=activity&site=stackoverflow&filter=!0Uv6ZT)teRUpIDUXg)eKBUB)K" %
                            question["question_id"], callback=self.parse_questions)
                    del item["questions"]

    def parse_questions(self, response):
        items = json.loads(response.content)
        if "items" in items:
            for item in items:
                owner_id = item["owner"]["user_id"]
                item["owner_id="] = owner_id
                question_id = item["question_id"]
                del item["owner"]
                stackoverflowdb.question.update({"question_id": question_id}, {"$set": item}, upsert=True)
                yield Request(
                    "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % owner_id,
                    callback=self.parse_users)
                if "answers" in item:
                    for answer in item["answers"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/answers/%s?order=desc&sort=activity&site=stackoverflow&filter=!LUcFBIwXAv-E7rc11-bLO." %
                            answer["answer_id"], callback=self.parse_answers)
                    del item["answers"]
                if "comments" in item:
                    for comment in item["comments"]:
                        yield Request(
                            "http://api.stackexchange.com/2.2/comments/%s?order=desc&sort=creation&site=stackoverflow&filter=!b0OfN.wWgRBMab" %
                            comment["comment_id"], callback=self.parse_comments)
                    del item["comments"]

    def parse_answers(self, response):
        items = json.loads(response.content)
        if "items" in items:
            for item in items:
                owner_id = item["owner"]["user_id"]
                item["owner_id="] = owner_id
                answer_id = item["answer_id"]
                stackoverflowdb.answer.update({"answer_id": answer_id}, {"$set": item}, upsert=True)
                yield Request(
                    "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % owner_id,
                    callback=self.parse_users)

    def parse_comments(self, response):
        items = json.loads(response.content)
        if "items" in items:
            for item in items:
                owner_id = item["owner"]["user_id"]
                item["owner_id="] = owner_id
                item["reply_to_user_id"] = reply_to_user_id
                reply_to_user_id = item["reply_to_user"]["user_id"]
                comment_id = item["comment_id"]
                del item["owner"]
                del item["reply_to_user"]
                stackoverflowdb.comment.update({"comment_id": comment_id}, {"$set": item}, upsert=True)
                yield Request(
                    "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % owner_id,
                    callback=self.parse_users)
                yield Request(
                    "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" % reply_to_user_id,
                    callback=self.parse_users)
