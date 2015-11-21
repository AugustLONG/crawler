# coding=utf-8
import re
import logging
from urlparse import urlparse

import scrapy
from bs4 import BeautifulSoup

import unirest
# from crawler.items import UserItem, BookItem


class ShaishufangSpider(scrapy.Spider):
    name = "Shaishufang"
    allowed_domains = ["shaishufang.com"]
    start_urls = []

    cookie = {
        'shaishufang': 'Mjc5MTYwfGZmY2VmYzIyYmMxZjhlZThjNzgzYjFlOGIxOWUwODg2'
    }
    Proxies = []
    meta = {
        'proxy': 'http://104.155.70.207:8888'
    }

    urlPrefix = 'http://shaishufang.com/index.php/site/main/uid/'
    urlPostfix = '/status//category//friend/false'

    pagePostfix = '/friend/false/category//status//type//page/'
    bookUrlPrefix = 'http://shaishufang.com/index.php/site/detail/uid/'
    bookUrlPostfix = '/status//category/I/friend/false'

    userOrBook = 'User'

    # build start_urls list first
    def __init__(self):
        self.dynamicProxies()
        logging.info(self.Proxies)
        for i in range(1, 279653):
            self.start_urls.append(self.urlPrefix + str(i) + self.urlPostfix)

    def start_requests(self):
        for i in range(len(self.start_urls)):
            self.assignProxy()
            yield scrapy.Request(self.start_urls[i], self.parse, meta=self.meta, cookies=self.cookie)

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        userName = self.getUserName(soup)
        totalPages = self.getTotalPages(soup)
        totalBooks = self.getTotalBooks(soup)

        userItem = UserItem()
        userItem['UID'] = response.url.replace(self.urlPrefix, '').replace(self.urlPostfix, '')
        userItem['UserName'] = userName
        userItem['TotalBooks'] = totalBooks
        userItem['TotalPages'] = totalPages
        self.userOrBook = 'User'
        yield userItem

        UID = response.url.replace(self.urlPrefix, '').replace(self.urlPostfix, '')
        for page in range(1, totalPages + 1):
            url = self.urlPrefix + UID + self.pagePostfix + str(page)
            self.assignProxy()
            yield scrapy.Request(url, self.parsePage, meta=self.meta, cookies=self.cookie)

    def parsePage(self, response):
        soup = BeautifulSoup(response.body)
        uid = urlparse(response.url).path.split('/')[5]

        bids = self.getUbids(soup)
        for bid in bids:
            url = self.bookUrlPrefix + uid + '/ubid/' + bid + self.bookUrlPostfix
            self.assignProxy()
            yield scrapy.Request(url, self.parseBook, meta=self.meta, cookies=self.cookie)

    def parseBook(self, response):
        soup = BeautifulSoup(response.body)
        uid = urlparse(response.url).path.split('/')[5]
        ubid = urlparse(response.url).path.split('/')[7]

        ISBN = self.getISBN(soup)
        if ISBN:
            # BookItem 包含好多字段，这里只插入ISBN, UID, UBID
            bookItem = BookItem()
            bookItem['ISBN'] = ISBN
            bookItem['UID'] = uid
            bookItem['UBID'] = ubid
            self.userOrBook = 'Book'
            yield bookItem

    # 动态获取HTTP Proxies， 并填充到Proxies中
    def dynamicProxies(self):
        url = 'http://svip.kuaidaili.com/api/getproxy/?orderid=983980639044193&num=100&browser=1&protocol=1&method=1&sp1=1&quality=0&sort=0&format=json&sep=1'
        res = unirest.get(url, headers={"Accept": "application/json"})
        for proxy in res.body['data']['proxy_list']:
            self.Proxies.append('http://' + str(proxy))

    # 给meta的proxy赋值
    def assignProxy(self):
        if len(self.Proxies) == 0:
            self.dynamicProxies()

        self.meta['proxy'] = self.Proxies.pop()

    # 从书的详细页面获取ISBN
    def getISBN(self, soup):
        if not soup:
            return False

        if soup.find('div', {'id': 'attr'}):
            if len(soup.find('div', {'id': 'attr'}).find_all('li')) == 0:
                return False
            if "ISBN:" in soup.find('div', {'id': 'attr'}).find_all('li')[-1].text:
                return str(soup.find('div', {'id': 'attr'}).find_all('li')[-1].text.replace('ISBN:', ''))
            else:
                return False

        return False

    # 从书籍列表页面获取UBIDS
    def getUbids(self, soup):
        bids = []
        if not soup:
            return bids

        if soup.find('ul', {'id': 'booksList'}):
            if len(soup.find('ul', {'id': 'booksList'}).find_all('li')) == 0:
                return bids
            for item in soup.find('ul', {'id': 'booksList'}).find_all('li'):
                bids.append(item.attrs['id'])

        return bids

    # 从soup中获取username
    def getUserName(self, soup):
        if not soup:
            return False

        if soup.find('div', {'id': 'username'}):
            return soup.find('div', {'id': 'username'}).find('span').text

        return False

    # 从soup中获取总页数
    def getTotalPages(self, soup):
        if not soup:
            return 1

        if soup.find('ul', {'id': 'booksPage'}):
            if len(soup.find('ul', {'id': 'booksPage'}).find_all('li')) == 0:
                return 1

            return int(soup.find('ul', {'id': 'booksPage'}).find_all('li')[-2].text)

        return 1

    # 从soup中获取总藏书量
    def getTotalBooks(self, soup):
        if not soup:
            return 0

        if soup.find('ul', {'id': 'categoryList'}):
            if soup.find('ul', {'id': 'categoryList'}).find('li'):
                return int(re.sub(r'[^\x00-\x7F]+', ' ',
                                  soup.find('ul', {'id': 'categoryList'}).find('li').find('a').text).strip())

        return 0
