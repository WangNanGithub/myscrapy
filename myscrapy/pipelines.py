# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem


class MyscrapyPipeline(object):
    def process_item(self, item, spider):
        try:
            if len(item['title']) > 0:
                print '****************', item['title'][0]
        except Exception, e:
            print e
            pass
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item': item, 'index': item['image_urls'].index(image_url)})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = request.meta['index']  # 通过上面的index传递过来列表中当前下载图片的下标
        image_guid = str(index) + '.' + request.url.split('.')[-1]
        filename = 'full/%s/%s/%s' % (unicode(item['page_title']), unicode(item['title'][0]), image_guid)
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
