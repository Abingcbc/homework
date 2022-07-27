# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonMoviesItem(scrapy.Item):
    validation = scrapy.Field()
    ID = scrapy.Field()
    name = scrapy.Field()
    star_score = scrapy.Field()
    imdb_score = scrapy.Field()
    time_len = scrapy.Field()
    year = scrapy.Field()
    restrict_level = scrapy.Field()
    rent_price = scrapy.Field()
    buy_price = scrapy.Field()
    meta_info = scrapy.Field()

