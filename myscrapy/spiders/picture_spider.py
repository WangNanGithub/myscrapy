# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from myscrapy.items import MyscrapyItem


class PictureSpider(scrapy.Spider):
    name = 'picture_spider'
    allowed_domains = ['97kxs.com']
    start_urls = ['http://97kxs.com/html/article/index12300.html']

    rules = (
        Rule(LxmlLinkExtractor(attrs=('href', )), callback='parse'),
    )

    def parse(self, response):
        try:
            # print 'url : ', response.url
            urls = response.xpath('/html/body/div[8]/div/div[3]/img/@src').extract()
            title = response.xpath('/html/body/div[8]/div/div[3]/h1/text()').extract()

            item = MyscrapyItem()
            item['title'] = title
            item['urls'] = urls
            yield item

            page_urls = response.xpath('/html/body/div[8]/div/ul/span/a/@href').extract()
            print len(page_urls)
            for url in page_urls:
                if str(url).startswith('http') or str(url).startswith('HTTP'):
                    full_url = url
                else:
                    full_url = response.urljoin(url)
                yield Request(url=full_url, callback=self.parse)
        except Exception, e:
            print "ERROR : ", e
