# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from myscrapy.items import ImageItem


class PictureSpider(scrapy.Spider):
    name = 'picture_spider'
    allowed_domains = ['97kxs.com']
    start_urls = ['http://97kxs.com/index.html']

    rules = (
        Rule(LxmlLinkExtractor(attrs=('href', )), callback='parse'),
    )

    def parse(self, response):
        """
        获取图片各个分类的 URL 和 名称
        :param response: 
        :return: 
        """
        urls = response.xpath('//*[@id="header_box"]/div/ul[3]/li/a/@href').extract()
        page_titles = response.xpath('//*[@id="header_box"]/div/ul[3]/li/a/text()').extract()

        for url in urls:
            if str(url).startswith('http') or str(url).startswith('HTTP'):
                full_url = url
            else:
                full_url = response.urljoin(url)
            yield Request(url=full_url, meta={'page_title': page_titles[urls.index(url)]}, callback=self.get_page_url)

    def get_page_url(self, response):
        """
        获取页面 URL
        :param response: 
        :return: 
        """
        page_title = response.meta['page_title']
        urls = response.xpath('//html/body/div[8]/div/ul/li/a/@href').extract()
        for url in urls:
            if str(url).startswith('http') or str(url).startswith('HTTP'):
                full_url = url
            else:
                full_url = response.urljoin(url)
            yield Request(url=full_url, meta={'page_title': page_title}, callback=self.get_image)

    def get_image(self, response):
        """
        获取图片 URL
        :param response: 
        :return: 
        """
        try:
            page_title = response.meta['page_title']
            urls = response.xpath('/html/body/div[8]/div/div[3]/img/@src').extract()
            title = response.xpath('/html/body/div[8]/div/div[3]/h1/text()').extract()

            item = ImageItem()
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
                yield Request(url=full_url, meta={'item': item}, callback=self.get_image)
        except Exception, e:
            print "ERROR : ", e
