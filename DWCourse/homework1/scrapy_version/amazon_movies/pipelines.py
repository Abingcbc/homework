# -*- coding: utf-8 -*-
from amazon_movies.utils import *

class AmazonMoviesPipeline(object):
    def process_item(self, item, spider):
        write_result(item)
