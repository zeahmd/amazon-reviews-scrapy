# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    user_picture = scrapy.Field()
    user_name = scrapy.Field()
    review_title = scrapy.Field()
    review_date = scrapy.Field()
    review_data = scrapy.Field()
