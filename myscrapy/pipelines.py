# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import random
import urllib


class MyscrapyPipeline(object):

    def process_item(self, item, spider):
        try:
            if len(item['title']) > 0:
                print '****************', item['title'][0]
            # for url in item['urls']:
            #     print url
        except Exception, e:
            print e
            pass
        return item
