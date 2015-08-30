# coding=utf-8
import logging as log
from django.db.utils import IntegrityError
from scraper.models import SchedulerRuntime, ScraperElem
import hashlib, ntpath
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from django.conf import settings as djsettings
import datetime
from pymongo import errors
from pymongo.mongo_client import MongoClient
from pymongo.read_preferences import ReadPreference

VERSION = '0.9.0'


def not_set(string):
    """ Check if a string is None or ''
    :returns: bool - True if the string is empty
    """
    if string is None:
        return True
    elif string == '':
        return True
    return False

settings = get_project_settings()
redis = djsettings.REDIS
redis_unique_key = settings.get("REDIS_UNIQUE_KEY")


class AlibabaMongoDBPipeline(object):
    """ MongoDB pipeline class """
    # Default options
    config = {
        'uri': 'mongodb://localhost:27017',
        'fsync': False,
        'write_concern': 0,
        'database': 'alibaba',
        'collection': 'items',
        'replica_set': None,
        'unique_key': None,
        'buffer': None,
        'append_timestamp': False,
        'stop_on_duplicate': 0,
    }

    # Item buffer
    current_item = 0
    item_buffer = []

    # Duplicate key occurence count
    duplicate_key_count = 0

    def load_spider(self, spider):
        self.crawler = spider.crawler
        self.settings = spider.settings

        if not hasattr(spider, 'update_settings') and hasattr(spider, 'custom_settings'):
            self.settings.setdict(spider.custom_settings or {}, priority='project')

    def open_spider(self, spider):
        self.load_spider(spider)

        # Configure the connection
        self.configure()

        if self.config['replica_set'] is not None:
            connection = MongoClient(
                self.config['uri'],
                replicaSet=self.config['replica_set'],
                w=self.config['write_concern'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY_PREFERRED)
        else:
            # Connecting to a stand alone MongoDB
            connection = MongoClient(
                self.config['uri'],
                fsync=self.config['fsync'],
                read_preference=ReadPreference.PRIMARY)

        # Set up the collection
        database = connection[self.config['database']]
        self.collection = database[self.config['collection']]
        log.msg(u'Connected to MongoDB {0}, using "{1}/{2}"'.format(
            self.config['uri'],
            self.config['database'],
            self.config['collection']))

        # Ensure unique index
        if self.config['unique_key']:
            self.collection.ensure_index(self.config['unique_key'], unique=True)
            log.msg('uEnsuring index for key {0}'.format(
                self.config['unique_key']))

        # Get the duplicate on key option
        if self.config['stop_on_duplicate']:
            tmpValue = self.config['stop_on_duplicate']
            if tmpValue < 0:
                log.msg(
                    (
                        u'Negative values are not allowed for'
                        u' MONGODB_STOP_ON_DUPLICATE option.'
                    ),
                    level=log.ERROR
                )
                raise SyntaxError(
                    (
                        'Negative values are not allowed for'
                        ' MONGODB_STOP_ON_DUPLICATE option.'
                    )
                )
            self.stop_on_duplicate = self.config['stop_on_duplicate']
        else:
            self.stop_on_duplicate = 0

    def configure(self):
        """ Configure the MongoDB connection """
        # Handle deprecated configuration
        if not not_set(self.settings['MONGODB_HOST']):
            log.msg(
                u'DeprecationWarning: MONGODB_HOST is deprecated',
                level=log.WARNING)
            mongodb_host = self.settings['MONGODB_HOST']

            if not not_set(self.settings['MONGODB_PORT']):
                log.msg(
                    u'DeprecationWarning: MONGODB_PORT is deprecated',
                    level=log.WARNING)
                self.config['uri'] = 'mongodb://{0}:{1:i}'.format(
                    mongodb_host,
                    self.settings['MONGODB_PORT'])
            else:
                self.config['uri'] = 'mongodb://{0}:27017'.format(mongodb_host)

        if not not_set(self.settings['MONGODB_REPLICA_SET']):
            if not not_set(self.settings['MONGODB_REPLICA_SET_HOSTS']):
                log.msg(
                    (
                        u'DeprecationWarning: '
                        u'MONGODB_REPLICA_SET_HOSTS is deprecated'
                    ),
                    level=log.WARNING)
                self.config['uri'] = 'mongodb://{0}'.format(
                    self.settings['MONGODB_REPLICA_SET_HOSTS'])

        # Set all regular options
        options = [
            ('uri', 'MONGODB_URI'),
            ('fsync', 'MONGODB_FSYNC'),
            ('write_concern', 'MONGODB_REPLICA_SET_W'),
            ('database', 'MONGODB_DATABASE'),
            ('collection', 'MONGODB_COLLECTION'),
            ('replica_set', 'MONGODB_REPLICA_SET'),
            ('unique_key', 'MONGODB_UNIQUE_KEY'),
            ('buffer', 'MONGODB_BUFFER_DATA'),
            ('append_timestamp', 'MONGODB_ADD_TIMESTAMP'),
            ('stop_on_duplicate', 'MONGODB_STOP_ON_DUPLICATE')
        ]

        for key, setting in options:
            if not not_set(self.settings[setting]):
                self.config[key] = self.settings[setting]

        # Check for illegal configuration
        if self.config['buffer'] and self.config['unique_key']:
            log.msg(
                (
                    u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                    u'and MONGODB_UNIQUE_KEY is not supported'
                ),
                level=log.ERROR)
            raise SyntaxError(
                (
                    u'IllegalConfig: Settings both MONGODB_BUFFER_DATA '
                    u'and MONGODB_UNIQUE_KEY is not supported'
                ))

    def process_item(self, item, spider):
        """ Process the item and add it to MongoDB
        :type item: Item object
        :param item: The item to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        item = dict(self._get_serialized_fields(item))
        item['site'] = self.conf["SITE"]
        item['website_id'] = self.conf["WEBSITE_ID"]
        item['website'] = self.conf["WEBSITE"]
        item['category'] = self.conf["CATEGORY"]
        item['scraper'] = self.conf["SCRAPER"]
        item['updated']=datetime.datetime.utcnow()
        checker_rt = SchedulerRuntime(runtime_type='C')
        checker_rt.save()
        item['checker_runtime_pk'] = checker_rt.pk
        # item.save() 数据保存
        spider.action_successful = True
        redis.sadd(redis_unique_key, item["unique_key"])

        if self.config['buffer']:
            self.current_item += 1

            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

            self.item_buffer.append(item)

            if self.current_item == self.config['buffer']:
                self.current_item = 0
                return self.insert_item(self.item_buffer, spider)

            else:
                return item
        return self.insert_item(item, spider)

    def close_spider(self, spider):
        """ Method called when the spider is closed
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: None
        """
        if self.item_buffer:
            self.insert_item(self.item_buffer, spider)

    def insert_item(self, item, spider):
        """ Process the item and add it to MongoDB
        :type item: (Item object) or [(Item object)]
        :param item: The item(s) to put into MongoDB
        :type spider: BaseSpider object
        :param spider: The spider running the queries
        :returns: Item object
        """
        if not isinstance(item, list):
            item = dict(item)

            if self.config['append_timestamp']:
                item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

        if self.config['unique_key'] is None:
            try:
                self.collection.insert(item, continue_on_error=True)
                log.msg(
                    u'Stored item(s) in MongoDB {0}/{1}'.format(
                        self.config['database'], self.config['collection']),
                    level=log.DEBUG,
                    spider=spider)
            except errors.DuplicateKeyError:
                log.msg(u'Duplicate key found', level=log.DEBUG)
                if (self.stop_on_duplicate > 0):
                    self.duplicate_key_count += 1
                    if (self.duplicate_key_count >= self.stop_on_duplicate):
                        self.crawler.engine.close_spider(
                            spider,
                            'Number of duplicate key insertion exceeded'
                        )
                pass

        else:
            key = {}
            if isinstance(self.config['unique_key'], list):
                for k in dict(self.config['unique_key']).keys():
                    key[k] = item[k]
            else:
                key[self.config['unique_key']] = item[self.config['unique_key']]

            self.collection.update(key, item, upsert=True)

            log.msg(
                u'Stored item(s) in MongoDB {0}/{1}'.format(
                    self.config['database'], self.config['collection']),
                level=log.DEBUG,
                spider=spider)
            spider.log("Item saved.", log.INFO)
        return item

class AlibabaImagesPipeline(ImagesPipeline):
    def __init__(self, *args, **kwargs):
        super(AlibabaImagesPipeline, self).__init__(*args, **kwargs)

    def get_media_requests(self, item, info):
        try:
            img_elems = info.spider.scraper.get_image_elems()
            for img_elem in img_elems:
                if img_elem.scraped_obj_attr.name in item and item[img_elem.scraped_obj_attr.name]:
                    if not hasattr(self, 'conf'):
                        self.conf = info.spider.conf
                    url = item[img_elem.scraped_obj_attr.name]
                    return Request(url,meta={"img_elem.scraped_obj_attr.name": img_elem.scraped_obj_attr.name})
        except (ScraperElem.DoesNotExist, TypeError):
            pass

    def image_key(self, url):
        image_guid = hashlib.sha1(url).hexdigest()
        if self.conf["IMAGES_STORE_FORMAT"] == 'FLAT':
            return '%s.jpg' % (image_guid)
        elif self.conf["IMAGES_STORE_FORMAT"] == 'THUMBS':
            return '%s/thumbs/%s/%s.jpg' % (self.conf["IMAGE_PATH"],self.THUMBS.iterkeys().next(), image_guid)
        else:
            return '%s/full/%s.jpg' % (self.conf["IMAGE_PATH"],image_guid)

    def thumb_key(self, url, thumb_id):
        image_guid = hashlib.sha1(url).hexdigest()
        if self.conf["IMAGES_STORE_FORMAT"] == 'FLAT':
            return '%s.jpg' % (image_guid)
        else:
            return '%s/thumbs/%s/%s.jpg' % (self.conf["IMAGE_PATH"],thumb_id, image_guid)

    def item_completed(self, results, item, info):
        try:
            img_elems = info.spider.scraper.get_image_elems()
        except ScraperElem.DoesNotExist:
            return item
        for img_elem in img_elems:
            results_list = [x for ok, x in results if ok]
            if len(results_list) > 0:
                item[img_elem.scraped_obj_attr.name] = ntpath.basename(results_list[0]['path'])
            else:
                item[img_elem.scraped_obj_attr.name] = None
        return item


class ValidationPipeline(object):

    def process_item(self, item, spider):
        # Check if item is double and remove DOUBLE string from ID fields
        #(no good way found to pass meta data to this point...)
        idf_elems = spider.scraper.get_id_field_elems()
        is_double = False
        exist_objects = spider.scraped_obj_class.objects
        for idf_elem in idf_elems:
            idf_name = idf_elem.scraped_obj_attr.name
            if idf_name in item and item[idf_name][0:6] == 'DOUBLE':
                is_double = True
                item[idf_name] = item[idf_name][6:]
                # exist_objects = exist_objects.filter(**{idf_name: item[idf_name]})

        if is_double:
            mandatory_elems = spider.scraper.get_standard_update_elems()
        else:
            mandatory_elems = spider.scraper.get_mandatory_scrape_elems()
        for elem in mandatory_elems:
            if not elem.scraped_obj_attr.name in item or \
                    (elem.scraped_obj_attr.name in item and not item[elem.scraped_obj_attr.name]):
                spider.log("Mandatory elem " + elem.scraped_obj_attr.name + " missing!", log.ERROR)
                raise DropItem()

        if spider.conf['MAX_ITEMS_SAVE'] and spider.items_save_count >= spider.conf['MAX_ITEMS_SAVE']:
            spider.log("Max items save reached, item not saved.", log.INFO)
            raise DropItem()

        if not spider.conf['DO_ACTION']:
            spider.log("TESTMODE: Item not saved.", log.INFO)
            raise DropItem()

        if is_double:
            standard_update_elems = spider.scraper.get_standard_update_elems()
            updated_attribute_list = ''
            exist_objects=[]
            if len(standard_update_elems) > 0 and len(exist_objects) == 1:
                exist_object = exist_objects[0]
                dummy_object = spider.scraped_obj_class()
                for elem in standard_update_elems:
                    attr_name = elem.scraped_obj_attr.name
                    if attr_name in item and hasattr(exist_object, attr_name):
                        setattr(dummy_object, attr_name, item[attr_name])
                        if unicode(getattr(dummy_object, attr_name)) != unicode(getattr(exist_object, attr_name)):
                            setattr(exist_object, attr_name, item[attr_name])
                            if len(updated_attribute_list) > 0:
                                updated_attribute_list += ', '
                            updated_attribute_list += attr_name
            if len(updated_attribute_list) > 0:
                exist_object.save()
                raise DropItem("Item already in DB, attributes updated: " + updated_attribute_list)
            else:
                raise DropItem("Double item.")

        spider.items_save_count += 1

        return item