# -*- coding: utf-8 -*-
import scrapy
from amazon_movies.items import AmazonMoviesItem
from bs4 import BeautifulSoup
import re
import amazon_movies.spiders.prime_parser as prime_parser
import amazon_movies.spiders.ordinary_parser as ordinary_parser
from amazon_movies.items import AmazonMoviesItem
import os
from scrapy.http import Request
import random
import requests
import amazon_movies.utils as utils
import urllib
from imageRecognize.imageRec import parse_robot
from amazon_movies.utils import *
import traceback
import threading
from scrapy.http.cookies import CookieJar

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = [
    ]
    cookieJar = CookieJar()

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        with open('to_find.txt', 'r') as file:
            count = 0
            for line in file:
                # if count > 100:
                #     break
                # count += 1
                if len(line.strip()) == 0:
                    continue
                self.start_urls.append('https://'+self.allowed_domains[0]+'/dp/'+line.strip())

    def parse(self, response):
        item = AmazonMoviesItem()
        print('Get page ' + str(response.url) + ' ' + str(response.request.meta['proxy']))
        proxy = response.request.meta['proxy'].replace('http://','')
        content = BeautifulSoup(response.body, 'lxml')
        item['ID'] = response.url
        item['ID'] = item['ID'].split('/')[-1].strip()
        if response.status == 404:
            item['validation'] = False
            yield item
        # If this film is banned by robot check, try it again.
        elif not content.find(name='title', text=re.compile('Robot Check')) is None:
            print ('Robot check triggered')
            try:
                print('-'*10+' Delete Proxy '+'-'*10)
                requests.get('http://127.0.0.1:5010/delete?proxy=' + proxy)
                yield scrapy.Request(response.url)
            #     thread_id = str(threading.currentThread().ident)
            #     urllib.request.urlretrieve(content.find(name='div', attrs={'class':'a-row a-text-center'}).
            #     find(name='img',attrs={'src':True})['src'], item['ID'] + '.jpg')
            #     capt_string = parse_robot(item['ID'] + '.jpg', item['ID'])
            #     os.remove(item['ID'] + '.jpg')
            #     print('remove ' + item['ID'] + '.jpg')
            #     if capt_string == "error":
            #         yield scrapy.Request(response.url, dont_filter=True)
            #     else:
            #         data = {'field-keywords': capt_string}
            #         robot_retry = scrapy.FormRequest.from_response(response, formdata=data, 
            #         callback=self.parse, #dont_filter=True,
            #         meta={'robot':1,'proxy':response.request.meta['proxy']}
            #         )
            #         yield robot_retry
            except Exception as e:
                with open('error.log','a') as file:
                    file.write(item['ID'])
                    file.write(traceback.format_exc())
                    file.write('\n')
                if type(e) is AttributeError:
                    with open('not_movie_id.txt','a') as file:
                        file.write(item['ID'])
        else:
            page_type = content.find(id='productTitle')
            if page_type is None:
                # print('-'*10 + item['ID'] + ': Prime' + '-'*10)
                item['name'], item['star_score'], item['imdb_score'], \
                item['time_len'], item['year'], item['restrict_level'], \
                item['rent_price'], item['buy_price'], item['meta_info'], \
                item['validation'] = prime_parser.prime_parse(content, item['ID'])
                yield item
            else:
                # print('-'*10 + item['ID'] + ': Ordinary' + '-'*10)
                item['name'], item['star_score'], item['imdb_score'], \
                item['time_len'], item['year'], item['restrict_level'], \
                item['rent_price'], item['buy_price'], item['meta_info'], \
                item['validation'] = ordinary_parser.ordinary_parse(content, item['ID'])
                yield item

        
