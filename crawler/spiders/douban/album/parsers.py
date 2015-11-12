#encoding: utf-8
import re

from items import AlbumItem, PhotoItem

FOLLOW_RE = re.compile(ur"(\d+)人关注")
PHOTO_COUNT_RE = re.compile(ur"(\d+)张照片")
CREATE_DATE_RE = re.compile(ur"\d{4}-\d{2}-\d{2}")

class ParentParser(object):
    def __init__(self, response):
        self.response = response

class AlbumParser(ParentParser):
    def __init__(self, response):
        ParentParser.__init__(self, response)
        self.next_page = False
        self.item = AlbumItem()

        self.get_from_url()
        if self.next_page: return

        self.get_album_name()
        self.get_author()
        self.get_recommend_total()
        self.get_like_total()
        self.get_tags()

        self.parse_short_info()
        self.get_create_date()
        self.get_photo_count()
        self.get_follow_count()
        self.get_desc()

    def get_from_url(self):
        url = self.response.url.split("?", 1)
        if len(url) > 1: self.next_page = True
        self.item["from_url"] = url[0]

    def get_album_name(self):
        x_album_name = self.response.xpath("//h1/text()").extract()[0].split("-", 1)
        if len(x_album_name) == 2: 
            self.item["album_name"] = x_album_name[1]
            author = self.item.setdefault("author", {})
            author["nickname"] = x_album_name[0].replace(u"的相册", "")

    def get_author(self):
        x_author = self.response.xpath("//div[@id='db-usr-profile']/div[@class='pic']/a")
        if x_author:
            author = self.item.setdefault("author", {})
            author["home_page"] = x_author.xpath("@href").extract()[0]
            author["avatar"] = x_author.xpath("img/@src").extract()[0]

    def get_recommend_total(self):
        x_recommend_total = self.response.xpath("//span[@class='rec-num']").re("\d+")
        if x_recommend_total: self.item["recommend_total"] = int( x_recommend_total[0] )

    def get_like_total(self):
        x_like_total = self.response.xpath("//span[@class='fav-num']/a/text()").re("\d+")
        if x_like_total: self.item["like_total"] = int( x_like_total[0] )

    def get_tags(self):
        x_tags = self.response.xpath("//div[@class='footer-tags']/a/text()").extract()
        if x_tags: self.item["tags"] = x_tags

    def parse_short_info(self):
        self.short_info = "".join(self.response.xpath("//div[@class='wr']//text()").extract())

    def get_create_date(self):
        M = CREATE_DATE_RE.search( self.short_info )
        if M is not None: self.item["create_date"] = M.group(0)

    def get_photo_count(self):
        M = PHOTO_COUNT_RE.search( self.short_info )
        if M is not None: self.item["photo_count"] = int( M.group(1) )

    def get_follow_count(self):
        M = FOLLOW_RE.search( self.short_info )
        if M is not None: self.item["follow_count"] = int( M.group(1) )

    def get_desc(self):
        x_desc = self.response.xpath("//div[@id='link-report']/text()").extract()
        if x_desc: self.item["desc"] = x_desc[0]


class SinglePhotoParser(ParentParser):
    def __init__(self, response):
        ParentParser.__init__(self, response)
        self.item = PhotoItem()
        self.from_url = None

        self.get_from_url()
        self.get_large_img_url()
        self.get_like_count()
        self.get_recommend_count()
        self.get_desc()

    def get_from_url(self):
        x_from_url = self.response.xpath("//div[@id='image']/span[@class='rr']/a/@href").extract()
        if x_from_url: self.from_url = x_from_url[0].split("?", 1)[0]

    def get_large_img_url(self):
        x_large_img_url =  self.response.xpath("//a[@class='mainphoto']/img/@src").extract()
        if x_large_img_url: self.item["large_img_url"] = x_large_img_url[0]

    def get_like_count(self):
        x_like_count = self.response.xpath("//span[@class='fav-num']/a/text()").re("\d+")
        if x_like_count: self.item["like_count"] = int( x_like_count[0] )

    def get_recommend_count(self):
         x_rec_num = self.response.xpath("//span[@class='rec-num']/text()").re("\d+")
         if x_rec_num: self.item["recommend_count"] = int( x_rec_num[0] )

    def get_desc(self):
        x_desc =  self.response.xpath("//div[@class='edtext pl']/text()").extract()
        if x_desc: self.item["desc"] = x_desc[0]


class CommentParser(ParentParser):
    def __init__(self, response):
        ParentParser.__init__(self, response)

    def get_comments(self):
        comments = []
        x_comments = self.response.xpath("//div[@class='comment-item']")
        for comment in x_comments:
            comment_dict = {}

            x_homepage = comment.xpath("div[@class='pic']/a/@href").extract()
            if x_homepage: comment_dict["home_page"] = x_homepage[0]

            x_avatar = comment.xpath("div[@class='pic']/a/img/@src").extract()
            if x_avatar: comment_dict["avatar"] = x_avatar[0]

            find_path = "div[@class='content report-comment']/div[@class='author']/span[1]/text()"
            x_post_datetime = comment.xpath(find_path).extract()
            if x_post_datetime: comment_dict["post_datetime"] = x_post_datetime[0]

            find_path = "div[@class='content report-comment']/div[@class='author']/a[1]/text()"
            x_nickname = comment.xpath(find_path).extract()
            if x_nickname: comment_dict["nickname"] = x_nickname[0]

            x_content = comment.xpath("div[@class='content report-comment']/p[1]/text()").extract()
            if x_content: comment_dict["content"] = x_content[0]

            comments.append( comment_dict )

        return comments