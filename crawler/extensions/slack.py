# -*- coding: utf-8 -*- #
"""
Created on 2015-11-22
@author: 李飞飞
"""
"""
SLACK_API_TOKEN = 'your key'
SLACK_CHANNEL = 'your channel'
SLACK_BOT = 'bot name'
EXTENSIONS = {'crawler.extensions.statstoslack.SlackStats': 100}
"""
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from slacker import Slacker
from scrapy.exceptions import NotConfigured

class SlackStats(object):

    def __init__(self, slack_api_token, channel, bot):
        self.slack = Slacker(slack_api_token)
        self.channel = channel
        self.bot = bot

    @classmethod
    def from_crawler(cls, crawler):
        slack_api_token = crawler.settings.getlist("SLACK_API_TOKEN")
        channel = crawler.settings.getlist("SLACK_CHANNEL")
        bot = crawler.settings.getlist("SLACK_BOT")
        if (not slack_api_token or not channel or not bot):
            raise NotConfigured
        ext = cls(slack_api_token, channel, bot)
        crawler.signals.connect(ext.start_stats, signal=signals.spider_opened)
        crawler.signals.connect(ext.finish_stats, signal=signals.stats_spider_closed)
        return ext

    def start_stats(self, spider):
        attachments = [
                {
                    "title": spider.name+" has begun.",
                    "fallback": spider.name+" has begun.",
                    "color": "good",
                }
            ]
        self.slack.chat.post_message(channel='#'+str(self.channel[0]), text=None, icon_emoji=":+1:", username=self.bot[0], attachments=attachments)

    def finish_stats(self, spider, spider_stats):
        if spider_stats['finish_reason'].encode('utf-8') == 'finished':
            color = "good"
            emoji = ":white_check_mark:"
        else:
            color = "bad"
            emoji = ":no_entry_sign:"

        attachments = [
                {
                    "title": spider.name+" has finished.",
                    "fallback": spider.name+" has finished.",
                    "color": color,
                    "mrkdwn_in": ["text", "pretext"],
                    "fields": [
                        {
                            "title": "start time",
                            "value": unicode(spider_stats['start_time'].replace(microsecond=0)),
                            "short": True
                        },
                        {
                            "title": "end time",
                            "value": unicode(spider_stats['finish_time'].replace(microsecond=0)),
                            "short": True
                        },
                        {
                            "title": "finish reason",
                            "value": spider_stats['finish_reason'].encode('utf-8'),
                            "short": True
                        },
                        {
                            "title": "items scraped",
                            "value": spider_stats['item_scraped_count'] if 'item_scraped_count' in spider_stats  else "0",
                            "short": True
                        },
                        {
                            "title": "request count",
                            "value": spider_stats['downloader/request_count'] if 'request_count' in spider_stats  else "0",
                            "short": True
                        },
                        {
                            "title": "response count",
                            "value": spider_stats['downloader/response_count'] if 'downloader/response_count' in spider_stats  else "0",
                            "short": True
                        },
                       {
                            "title": "200 count",
                            "value": spider_stats['downloader/response_status_count/200'] if 'downloader/response_status_count/200' in spider_stats else "0",
                            "short": True
                        },
                        {
                            "title": "301 count",
                            "value": spider_stats['downloader/response_status_count/301'] if 'downloader/response_status_count/301' in spider_stats else "0",
                            "short": True
                        },
                       {
                            "title": "404 count",
                            "value": spider_stats['downloader/response_status_count/404'] if 'downloader/response_status_count/404' in spider_stats else "0",
                            "short": True
                        },
                        {
                            "title": "500 count",
                            "value": spider_stats['downloader/response_status_count/500'] if 'downloader/response_status_count/500' in spider_stats else "0",
                            "short": True
                        }

                    ],
            }
            ]
        self.slack.chat.post_message(channel='#'+str(self.channel[0]), text=None, icon_emoji=emoji, username=self.bot[0], attachments=attachments)
        return