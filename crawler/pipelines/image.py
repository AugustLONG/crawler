
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


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
        image_info = self.upyun.getFileInfo(self.prefix+'/'+key)
        last_modified = int(image_info['date'])
        checksum = image_info['size']
        return {'last_modified': last_modified, 'checksum': checksum}

    def persist_image(self, key, image, buf, info):
        tmp_path = os.path.join(self.TMP_PATH, 'tmp.jpg')
        image.save(tmp_path)
        data = open(tmp_path, 'rb')
        self.upyun.setContentMD5(md5file(data))
        # fiel secret
        self.upyun.setFileSecret('')
        result = self.upyun.writeFile(self.prefix+'/'+key, data, True)
        if not result:
            log.msg("Image: Upload image to Upyun Failed! %s" % (self.prefix+key))

class GetimagesprojectPipeline(ImagesPipeline):
    ImagesPipeline.STORE_SCHEMES['http'] = UpYunStore
    URL_PREFIX = None

    def set_filename(self, response):
        #add a regex here to check the title is valid for a filename.
        return 'full/{0}.jpg'.format(response.meta['pid'])

    def get_media_requests(self, item, info):
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        for image_url in item['image_urls']:
                yield scrapy.Request(image_url, meta={'pid': item['pid']})

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
        image_info = self.upyun.getFileInfo(self.prefix+'/'+key)
        return super(CoverImagesPipeline, cls).from_settings(settings)

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
        image_info = self.upyun.getFileInfo(self.prefix+'/'+key)