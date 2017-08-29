# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from myscrapy.items import MyscrapyItem


class PictureSpider(scrapy.Spider):
    name = 'picture_spider'
    allowed_domains = ['97kxs.com']
    start_urls = ['http://97kxs.com/index.html']

    rules = (
        Rule(LxmlLinkExtractor(attrs=('href', )), callback='parse'),
    )

    def parse(self, response):
        # //*[@id="header_box"]/div/ul[2]/li/a/@href
        urls = response.xpath('//*[@id="header_box"]/div/ul[3]/li/a/@href').extract()
        page_titles = response.xpath('//*[@id="header_box"]/div/ul[3]/li/a/text()').extract()

        for url in urls:
            if str(url).startswith('http') or str(url).startswith('HTTP'):
                full_url = url
            else:
                full_url = response.urljoin(url)
            print page_titles[urls.index(url)]
            yield Request(url=full_url, meta={'page_title': page_titles[urls.index(url)]}, callback=self.parse1)

    def parse1(self, response):

        # /html/body/div[8]/div/ul/li[1]/a
        page_title = response.meta['page_title']
        urls = response.xpath('//html/body/div[8]/div/ul/li/a/@href').extract()
        for url in urls:
            if str(url).startswith('http') or str(url).startswith('HTTP'):
                full_url = url
            else:
                full_url = response.urljoin(url)
            yield Request(url=full_url, meta={'page_title': page_title}, callback=self.parse2)

    def parse2(self, response):
        try:
            page_title = response.meta['page_title']
            urls = response.xpath('/html/body/div[8]/div/div[3]/img/@src').extract()
            title = response.xpath('/html/body/div[8]/div/div[3]/h1/text()').extract()

            item = MyscrapyItem()
            item['title'] = title
            item['page_title'] = page_title
            item['image_urls'] = urls
            yield item

            page_urls = response.xpath('/html/body/div[8]/div/ul/span/a/@href').extract()
            for url in page_urls:
                if str(url).startswith('http') or str(url).startswith('HTTP'):
                    full_url = url
                else:
                    full_url = response.urljoin(url)
                yield Request(url=full_url, meta={'item': item}, callback=self.parse2)
        except Exception, e:
            print "ERROR : ", e
