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
            url = item['url'][0].replace('http://img.diercun.com/hd', 'https://mpic.24meinv.me/hd')
            filename = "/Users/wangnan/Github/myscrapy/images/" + item['name'][0].encode('utf-8') + str(int(random.random() * 10000)) + ".jpg"
            print '----------------------'
            print '----------------------'
            # http://img.diercun.com/hd/YouMi/Vol.053/053_005_zp0_3600_5400.jpg
            # https://mpic.24meinv.me/hd/YouMi/Vol.053/053_005_zp0_3600_5400.jpg
            # https://mpic.24meinv.me/hd/YouMi/Vol.053/053_002_9jm_3600_5400.jpg
            # 目前不会下载 https 开头的图片
            res = urllib.urlopen(url)
            print res
            print 'url : ', url
            print 'filename : ', filename
            print '----------------------'
            print '----------------------'
            with open(filename, 'wb') as f:
                f.write(res.read())
            # pic = requests.get(url)
            # with open(filename, 'wb') as fp:
            #     fp.write(pic.content)
        except Exception, e:
            print e
            pass
        return item
