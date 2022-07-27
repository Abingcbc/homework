# -*- coding: utf-8 -*-

import scrapy
from scrapy import signals
import random
import time
import requests
from amazon_movies.utils import *
import traceback

class AmazonMoviesDownloaderMiddleware(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_request(self, request, spider):
        new_request(request, spider)
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            if response.status == 404:
                with open("404.log", "a") as file:
                    file.write(response.url.split('/')[-1].strip() + "\n")
                    return response
            log('ErrorCode: ' + str(response.status) + ' ' + str(response.url))
            if request.url.find('errors') >= 0:
                raise scrapy.exceptions.IgnoreRequest
            print('-'*10+' Delete Proxy '+'-'*10)
            requests.get('http://127.0.0.1:5010/delete?proxy=' + 
            request.meta['proxy'].replace('http://',''))
            return new_request(request, spider)
        return response

    def process_exception(self, request, exception, spider):
        # log('MyError: ' + request.url + ' ' + str(exception))
        # with open('error.log', 'a') as file:
        #     file.write(request.url + '\n')
        #     file.write(traceback.format_exc())
        #     file.write('\n')
        if not exception is AttributeError:
            print('-'*10+' Delete Proxy '+'-'*10)
            requests.get('http://127.0.0.1:5010/delete?proxy='+
            request.meta['proxy'].replace('http://',''))
        return new_request(request, spider)