# encoding: utf-8
from random import choice
from random import randint

BID_LEN = 20
BID_LIST_LEN = 500


def gen_bids():
    bids = []
    for i in range(BID_LIST_LEN):
        bid = []
        for x in range(BID_LEN):
            bid.append(chr(randint(65, 90)))
        bids.append("".join(bid))
    return bids


class CustomCookieMiddleware(object):
    def __init__(self):
        self.bids = gen_bids()

    def process_request(self, request, spider):
        request.headers["Cookie"] = 'bid="%s"' % choice(self.bids)


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ug = "Baiduspider"
        request.headers["User-Agent"] = ug


class CustomHeadersMiddleware(object):
    def process_request(self, request, spider):
        request.headers["Accept-Language"] = "zh-CN,zh"
