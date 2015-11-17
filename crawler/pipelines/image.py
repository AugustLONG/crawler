import sys
import os

from scrapy.conf import settings

reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import logging as log
import hashlib, ntpath
from upyun import UpYun


class UpYunStore(object):
    APP_NAME = None
    USERNAME = None
    PASSWORD = None
    TMP_PATH = None

    def __init__(self, uri):
        assert uri.startswith('http://')
        self.upyun = UpYun(self.APP_NAME, self.USERNAME, self.PASSWORD)
        self.prefix = '/' + uri.split('/')[-1]

    def stat_image(self, key, info):
        image_info = self.upyun.getinfo(self.prefix + '/' + key)
        last_modified = int(image_info['date'])
        checksum = image_info['size']
        return {'last_modified': last_modified, 'checksum': checksum}

    def persist_image(self, key, image, buf, info):
        tmp_path = os.path.join(self.TMP_PATH, 'tmp.jpg')
        image.save(tmp_path)
        data = open(tmp_path, 'rb')
        result = self.upyun.put(self.prefix + '/' + key, data, True)
        if not result:
            log.info("Image: Upload image to Upyun Failed! %s" % (self.prefix + key))


class GetimagesprojectPipeline(ImagesPipeline):
    ImagesPipeline.STORE_SCHEMES['http'] = UpYunStore
    URL_PREFIX = None

    def set_filename(self, response):
        # add a regex here to check the title is valid for a filename.
        return 'full/{0}.jpg'.format(response.meta['pid'])

    def get_media_requests(self, item, info):
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'pid': item['pid']})

    def get_images(self, response, request, info):
        for key, image, buf in super(GetimagesprojectPipeline, self).get_images(response, request, info):
            key = self.set_filename(response)
            yield key, image, buf

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    @classmethod
    def from_settings(cls, settings):
        upyun = cls.STORE_SCHEMES['http']
        upyun.APP_NAME = settings['UPYUN_APP_NAME']
        upyun.USERNAME = settings['UPYUN_USERNAME']
        upyun.PASSWORD = settings['UPYUN_PASSWORD']
        upyun.TMP_PATH = settings['TMP_PATH']
        cls.URL_PREFIX = settings['IMAGES_STORE']
        return super(GetimagesprojectPipeline, cls).from_settings(settings)

    @classmethod
    def from_settings(cls, settings):
        cls.MIN_WIDTH = settings.getint('IMAGES_MIN_WIDTH', 0)
        cls.MIN_HEIGHT = settings.getint('IMAGES_MIN_HEIGHT', 0)
        cls.EXPIRES = settings.getint('IMAGES_EXPIRES', 90)
        cls.THUMBS = settings.get('IMAGES_THUMBS', {})
        cls.IMAGES_URLS_FIELD = settings.get('IMAGES_URLS_FIELD', cls.DEFAULT_IMAGES_URLS_FIELD)
        cls.IMAGES_RESULT_FIELD = settings.get('IMAGES_RESULT_FIELD', cls.DEFAULT_IMAGES_RESULT_FIELD)
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri)


class CoverImagesPipeline(ImagesPipeline):
    ImagesPipeline.STORE_SCHEMES['http'] = UpYunStore
    URL_PREFIX = None

    @classmethod
    def from_settings(cls, settings):
        upyun = cls.STORE_SCHEMES['http']
        upyun.APP_NAME = settings['UPYUN_APP_NAME']
        upyun.USERNAME = settings['UPYUN_USERNAME']
        upyun.PASSWORD = settings['UPYUN_PASSWORD']
        upyun.TMP_PATH = settings['TMP_PATH']
        cls.URL_PREFIX = settings['IMAGES_STORE']
        return super(CoverImagesPipeline, cls).from_settings(settings)


class LocalImagesPipeline(ImagesPipeline):
    def __init__(self, *args, **kwargs):
        super(LocalImagesPipeline, self).__init__(*args, **kwargs)

    def get_media_requests(self, item, info):
        for url in item["urls"]:
            yield Request(url)

    def image_key(self, url):
        image_guid = hashlib.sha1(url).hexdigest()
        if self.conf["IMAGES_STORE_FORMAT"] == 'FLAT':
            return '%s.jpg' % (image_guid)
        elif self.conf["IMAGES_STORE_FORMAT"] == 'THUMBS':
            return '%s/thumbs/%s/%s.jpg' % (self.conf["IMAGE_PATH"], self.THUMBS.iterkeys().next(), image_guid)
        else:
            return '%s/full/%s.jpg' % (self.conf["IMAGE_PATH"], image_guid)

    def thumb_key(self, url, thumb_id):
        image_guid = hashlib.sha1(url).hexdigest()
        if self.conf["IMAGES_STORE_FORMAT"] == 'FLAT':
            return '%s.jpg' % (image_guid)
        else:
            return '%s/thumbs/%s/%s.jpg' % (self.conf["IMAGE_PATH"], thumb_id, image_guid)

    def item_completed(self, results, item, info):
        img_elems = info.spider.scraper.get_image_elems()
        for img_elem in img_elems:
            img_attr_name = img_elem.scraped_obj_attr.name
            for ok, x in results:
                if ok:
                    item[img_attr_name] = item[img_attr_name].replace(x['url'], ntpath.basename(x['path']))
                    results_list = [x for ok, x in results if ok]
            if len(results_list) == 0:
                item[img_attr_name] = None
        return item
