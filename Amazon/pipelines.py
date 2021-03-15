# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging


class AmazonPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        return item
