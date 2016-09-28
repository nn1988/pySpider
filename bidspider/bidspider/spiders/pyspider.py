# import os
# import re
import scrapy
import urllib2

from scrapy.selector import Selector
# from scrapy.item import spiderItem
# from scrapy.http import Request

class bidSpider(scrapy.Spider):
    name                = "BidSpider"
    allowed_domains     = ["www.chinabidding.com.cn"]
    start_urls          = ["https://www.chinabidding.cn/search/searchgj/zbcg?rp=30&categoryid=1%2C2&keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&page=1&areaid=5%2C6%2C&table_type=1%2C2%2C4%2C5%2C&search_type=TITLE&b_date=year"]

    def parse(self, response):
        # sel             = Selector(response)
        # postion         = sel.xpath('/html/body/div[1]/div[1]/div[12]/table/tbody').extract()
        # _url            = postion.xpath('//href')

        res = response.body
        FileTag = open(filename, 'w')
        FileTag.write(res)

