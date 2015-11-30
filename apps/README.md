# 大数据搜索
基于scrapy的采集系统，采用reids、kafka、celery、rabbitmq、elasticsearch、mysql、django等技术
打造新生代的数据搜索和数据基础平台

# Scrapy Cluster

This Scrapy project uses Redis and Kafka to create a distributed on demand scraping cluster.

The goal is to distribute seed URLs among many waiting spider instances, whose requests are coordinated via Redis. Any other crawls those trigger, as a result of frontier expansion or depth traversal, will also be distributed among all workers in the cluster.

The input to the system is a set of Kafka topics and the output is a set of Kafka topics. Raw HTML and assets are crawled interactively, spidered, and output to the log. For easy local development, you can also disable the Kafka portions and work with the spider entirely via Redis, although this is not recommended due to the serialization of the crawl requests.

## Dependencies

Please see `requirements.txt` for Pip package dependencies across the different sub projects.

Other important components required to run the cluster

- Python 2.7: https://www.python.org/downloads/
- Redis: http://redis.io
- Zookeeper: https://zookeeper.apache.org
- Kafka: http://kafka.apache.org

## Core Concepts

This project tries to bring together a bunch of new concepts to Scrapy and large scale distributed crawling in general. Some bullet points include:

- The spiders are dynamic and on demand, meaning that they allow the arbitrary collection of any web page that is submitted to the scraping cluster
- Scale Scrapy instances across a single machine or multiple machines
- Coordinate and prioritize their scraping effort for desired sites
- Persist across scraping jobs or have multiple scraping jobs going at the same time
- Allows for unparalleled access into the information about your scraping job, what is upcoming, and how the sites are ranked
- Allows you to arbitrarily add/remove/scale your scrapers from the pool without loss of data or downtime
- Utilizes Apache Kafka as a data bus for any application to interact with the scraping cluster (submit jobs, get info, stop jobs, view results)

## Documentation

Please check out our official [Scrapy Cluster documentation](http://scrapy-cluster.readthedocs.org/) for more details on how everything works!


## Redis Keys
The following keys within Redis are used by the Scrapy Cluster:

- timeout:<spiderid>:<appid>:<crawlid> - The timeout value of the crawl in the system, used by the Redis Monitor. The actual value of the key is the date in seconds since epoch that the crawl with that particular spiderid, appid, and crawlid will expire.
- <spiderid>:queue - The queue that holds all of the url requests for a spider type. Within this sorted set is any other data associated with the request to be crawled, which is stored as a Json object that is Pickle encoded.
- <spiderid>:dupefilter:<crawlid> - The duplication filter for the spider type and crawlid. This Redis Set stores a scrapy url hash of the urls the crawl request has already seen. This is useful for coordinating the ignoring of urls already seen by the current crawl request.
- <spiderid>:blacklist - A permanent blacklist of all stopped and expired crawlid‘s . This is used by the Scrapy scheduler prevent crawls from continuing once they have been halted via a stop request or an expiring crawl. Any subsequent crawl requests with a crawlid in this list will not be crawled past the initial request url.