# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem


title = ''
count = 0


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


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_type = request.url.split('.')[-1]
        print 'full/%s/%s' % (title, count)
        return 'full/%s/%s.%s' % (title, count, image_type)

    def get_media_requests(self, item, info):
        global title, count
        title = item['title'][0]
        count = 0
        for image_url in item['image_urls']:
            count = count + 1
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
