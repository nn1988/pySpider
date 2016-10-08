#
# pysider.py
# spidername = 'BidSpider'
#
# Created by Lee_np on 16/9/26.
# Copyright © 2016年 Lee_np. All rights reserved.
#
import os
import scrapy
import pymysql

from scrapy.selector import Selector
from bidspider.items import BidspiderItem
# from scrapy.http import Request


def _url_list():
    """ Return the init crawl list

    There is two situations. Maybe one url or many urls in the 'start_utl' list. This function will handle these two
    situation.

    Args:

    Return:
        A url list, can be empty, one or one more element
        _url:
    """

    _url = []
    _url.append("https://www.chinabidding.cn/search/searchzbw/search2?"
                "keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&table_type=&areaid=&categoryid=1&b_date=year")
    _url.append("https://www.chinabidding.cn/search/searchzbw/search2?rp=22&categoryid=1"
                "&keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&page=2&areaid=&table_type=0&b_date=year")
    str1 = ("https://www.chinabidding.cn/search/searchzbw/search2?rp=22&categoryid=1"
            "&keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&page=")
    str2 = "&areaid=&table_type=0&b_date=year"
    j = 1

    while j < 44:
        str_xy = str1 + str(j) + str2
        _url.append(str_xy)
        j += 1
    _url_thran = set(_url)
    _url = list(_url_thran)
    return _url


class BidSpider(scrapy.Spider):

    name = "BidSpider"
    allowed_domains = ["www.chinabidding.com.cn"]

    start_urls = _url_list()

    def parse(self, response):
        sel = Selector(response)
        str_xpath_pre = '//*[@id="cTable"]/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr['
        str_xpath_ex = ']/td[2]/a/'
        begin_order = 2
        end_order = 44
        items = []
        file_tag = open('x.txt', 'w')
        while begin_order <= end_order:
            item = BidspiderItem()
            str_xpath = str_xpath_pre + str(begin_order) + str_xpath_ex
            url_trans = sel.xpath(str_xpath + '@href').extract()
            title_trans = sel.xpath(str_xpath + 'text()').extract()
            item['sigUrl'] = 'www.chinabidding.cn/' + url_trans[0].encode('utf-8')
            item['bidTitle'] = title_trans[0]
            begin_order += 2
            items.append(item)

        for i in items:
            file_tag.write(i['bidTitle'].encode('utf-8') + ',')
            file_tag.write(i['sigUrl'].encode('utf-8') + '\n')

        file_tag.close()
        # file_tag.write(items)

    def parse_write_to_file(self):
        if os.path.getsize('/Users/linaipeng/GitHub/pySpider/bidspider/bidspider/spiders/x.txt'):
            print('文件存在且不为空')

    def parse_opereate_mysql(self):
        """Open the mysql

        Two situations, local or remote MySQL
        """
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'c9122999',
            'db': 'bid_data',

        }
        # Connect to the database
        conn = pymysql.connect(config)
        cursor = conn.cursor() //游标
        close
        ('select * from call_bid')

