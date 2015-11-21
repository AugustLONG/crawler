# encoding: utf-8
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
import re, json, time
from pymongo import MongoClient

mongodb = MongoClient()
stackoverflowdb = mongodb.stackoverflow
key = "&key=U4DMV*8nvpm3EOpvf69Rxw(("


class StackoverflowSpider(CrawlSpider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com", "stackexchange.com"]
    question_url = "http://api.stackexchange.com/2.2/questions/%s?order=desc&sort=activity&site=stackoverflow&filter=!0Uv6ZT)teRUpIDUXg)eKBUB)K" + key
    comment_url = "http://api.stackexchange.com/2.2/comments/%s?order=desc&sort=creation&site=stackoverflow&filter=!-*f(6sqoFKmM" + key
    answer_url = "http://api.stackexchange.com/2.2/answers/%s?order=desc&sort=activity&site=stackoverflow&filter=!LUcFBdXEo-6Qzavr4yj3rc" + key
    user_url = "http://api.stackexchange.com/2.2/users/%s?order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv" + key

    def start_requests(self):
        for i in range(1, 500, 1):
            i = str(i)
            yield Request(
                'http://api.stackexchange.com/2.2/questions?page=' + i + '&pagesize=50&order=desc&sort=activity&site=stackoverflow&filter=!LUcFBE)pRrTKav*c.B*_WQ' + key,
                self.parse_questions)
            yield Request(
                'http://api.stackexchange.com/2.2/answers?page=' + i + '&pagesize=50&order=desc&sort=activity&site=stackoverflow&filter=!)rCcH8tl1NCISRRturSV' + key,
                self.parse_answers)
            yield Request(
                'http://api.stackexchange.com/2.2/users?page=' + i + '&pagesize=50&order=desc&sort=reputation&site=stackoverflow&filter=!-*f(6q9aL0dv' + key,
                self.parse_users)
            yield Request(
                'http://api.stackexchange.com/2.2/comments?page=' + i + '&pagesize=50&order=desc&sort=creation&site=stackoverflow&filter=!b0OfN.wWgRBMab' + key,
                self.parse_comments)
            yield Request(
                'http://api.stackexchange.com/2.2/tags?page=' + i + '&order=desc&sort=popular&site=stackoverflow&filter=!-*f(6qOIRTkE' + key,
                self.parse_tags)


    def delay(self, seconds=10):
        time.sleep(seconds)

    def _parse_all(self, comments=[], questions=[], users=[], answers=[]):
        for comment in comments:
            stackoverflowdb.comment.update({"comment_id": comment["comment_id"]}, {"$set": comment}, upsert=True)
            yield Request(self.comment_url % comment["comment_id"], callback=self.parse_comments)
        for question in questions:
            stackoverflowdb.question.update({"question_id": question["question_id"]}, {"$set": question}, upsert=True)
            yield Request(self.question_url % question["question_id"], callback=self.parse_questions)
        for answer in answers:
            stackoverflowdb.answer.update({"answer_id": answer["answer_id"]}, {"$set": answer}, upsert=True)
            yield Request(self.answer_url % answer["answer_id"], callback=self.parse_answers)
        for user in users:
            stackoverflowdb.user.update({"user_id": user["user_id"]}, {"$set": user}, upsert=True)
            yield Request(self.user_url % user["user_id"], callback=self.parse_users)

    def _parse_item(self, item, comments=[], questions=[], users=[], answers=[]):
        if "answers" in item:
            answers.extend(item["answers"])
            del item["answers"]
        if "comments" in item:
            comments.extend(item["comments"])
            del item["comments"]
        if "questions" in item:
            questions.extend(item["questions"])
            del item["questions"]
        if "owner" in item:
            users.append(item["owner"])
            del item["owner"]
        if "reply_to_user" in item:
            users.append(item["reply_to_user"])
            del item["reply_to_user"]
        if "last_editor" in item:
            users.append(item["last_editor"])
            item["last_editor_id"]=item["last_editor"]["user_id"]
            del item["last_editor"]
        if "bounty_user" in item:
            users.append(item["bounty_user"])
            item["bounty_user_id"]=item["bounty_user"]["user_id"]
            del item["bounty_user"]
        if "awarded_bounty_users" in item:
            users.extend(item["awarded_bounty_users"])
            del item["awarded_bounty_users"]
        return item, comments, questions, users, answers

    def parse_users(self, response):
        self.delay()
        items = json.loads(response.body)
        if "items" in items:
            answers, comments, questions, users = [], [], [], []
            for item in items["items"]:
                item, comments, questions, users, answers = self._parse_item(item, comments, questions, users, answers)
                stackoverflowdb.user.update({"user_id": item["user_id"]}, {"$set": item}, upsert=True)
            self._parse_all(comments=comments, questions=questions, answers=answers, users=users)

    def parse_questions(self, response):
        self.delay()
        items = json.loads(response.body)
        if "items" in items:
            answers, comments, questions, users = [], [], [], []
            for item in items["items"]:
                item, comments, questions, users, answers = self._parse_item(item, comments, questions, users, answers)
                stackoverflowdb.question.update({"question_id": item["question_id"]}, {"$set": item}, upsert=True)
            self._parse_all(comments=comments, questions=questions, answers=answers, users=users)

    def parse_answers(self, response):
        self.delay()
        items = json.loads(response.body)
        if "items" in items:
            answers, comments, questions, users = [], [], [], []
            for item in items["items"]:
                item, comments, questions, users, answers = self._parse_item(item, comments, questions, users, answers)
                stackoverflowdb.answer.update({"answer_id": item["answer_id"]}, {"$set": item}, upsert=True)
            self._parse_all(comments=comments, questions=questions, answers=answers, users=users)

    def parse_comments(self, response):
        self.delay()
        items = json.loads(response.body)
        if "items" in items:
            answers, comments, questions, users = [], [], [], []
            for item in items["items"]:
                item, comments, questions, users, answers = self._parse_item(item, comments, questions, users, answers)
                stackoverflowdb.comment.update({"comment_id": item["comment_id"]}, {"$set": item}, upsert=True)
            self._parse_all(comments=comments, questions=questions, answers=answers, users=users)

    def parse_tags(self, response):
        self.delay(3)
        items = json.loads(response.body)
        if "items" in items:
            for item in items["items"]:
                stackoverflowdb.tags.update({"name": item["name"]}, {"$set": item}, upsert=True)


