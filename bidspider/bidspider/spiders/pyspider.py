# coding: utf-8
# pysider.py
# spidername = 'BidSpider'
#
# Created by Lee_np on 16/9/26.
# Copyright 2016年 Lee_np. All rights reserved.
#


import os
import scrapy
import pymysql


from scrapy.selector import Selector
from bidspider.items import BidspiderItem
from scrapy.http import Request


def _url_list():
    """ Return the init crawl list

    There is two situations. Maybe one url or many urls in the 'start_utl' list. This function will handle these two
    situation.

    Args:

    Return:
        A url list, can be empty, one or one more element
        _url:
    """

    _url = [("https://www.chinabidding.cn/search/searchzbw/search2?"
             "keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&table_type=&areaid=&categoryid=1&b_date=year"),
            ("https://www.chinabidding.cn/search/searchzbw/search2?rp=22&categoryid=1"
             "&keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&page=2&areaid=&table_type=0&b_date=year")]
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
    _url.sort()
    return _url


def _tem_url_list():
    """Just for the test of Xpath"""

    _tem_url = [("https://www.chinabidding.cn/search/searchzbw/search2?"
                 "keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&table_type=&areaid=&categoryid=1&b_date=year")]
    return _tem_url


class BidSpider(scrapy.Spider):

    name = "BidSpider"
    allowed_domains = ["www.chinabidding.com.cn"]

    start_urls = _url_list()
    # start_urls = _tem_url_list()

    def parse(self, response):
        sel = Selector(response)
        str_xpath_pre = '//*[@id="cTable"]/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr['
        str_xpath_ex = ']/td[2]/a/'
        begin_order = 2
        items = []
        tag_for_xpath = 0
        while tag_for_xpath == 0:
            item = BidspiderItem()
            str_xpath = str_xpath_pre + str(begin_order) + str_xpath_ex
            url_trans = sel.xpath(str_xpath + '@href').extract()
            title_trans = sel.xpath(str_xpath + 'text()').extract()
            len_url_trans = 0
            # print title_trans, ', ', type(title_trans), ', ', len(title_trans)
            if len_url_trans == len(title_trans):
                break

            # This is the test module
            if begin_order == 60:
                tag_for_xpath = 1

            try:
                item['sigUrl'] = 'www.chinabidding.cn/' + url_trans[0].encode('utf-8')
                item['bidTitle'] = title_trans[0]
                begin_order += 2
                items.append(item)

            except IndexError:
                print 'Ops, Maybe the list index is wrong!'
                break

        BidSpider.parse_write_to_file('first', items)
        read_url_list = self.parse_read_urllist()
        for i in read_url_list:
            request = Request(i, self.parse_resolve())
            yield request
        return

    @classmethod
    def parse_read_urllist(cls, filename):
        """Get the usable url form TXT file

        Just for the test environment. The real code will operate with MySQL
        Args:
            filename: name of the temporary txt file of storage the url and bid title
        Return:
            _read_list: list of the result
        """

        _read_list = []
        if not os.path.exists(filename):
            print ('Ops, There is no exactly file! ')
            return False

        _input = open(filename)
        for line in _input:
            lines = line.split(',')
            _read_list.append(lines[1])

        return _read_list

    @classmethod
    def parse_write_to_file(cls, file_name, items):
        """Write the results into TXT file

        Args:
            file_name: name of the written files
            items: list of the results obtain from parse
        return:
            None
        """

        str_pre = '/Users/linaipeng/GitHub/pySpider/bidspider/bidspider/spiders/'
        str_ex = '.txt'
        str_file_name = str_pre + str(file_name) + str_ex
        if os.path.exists(str_file_name):
                print('文件存在且不为空')
                file_tag = open(str_file_name, 'a')
                for i in items:
                    file_tag.write(i['bidTitle'].encode('utf-8') + ',')
                    file_tag.write(i['sigUrl'].encode('utf-8') + '\n')
                file_tag.close()
        else:
            file_tag = open(str_file_name, 'w')
            print('创建文件' + file_name + '.txt')
            for i in items:
                file_tag.write(i['bidTitle'].encode('utf-8') + ',')
                file_tag.write(i['sigUrl'].encode('utf-8') + '\n')
            file_tag.close()

    def parse_resolve(self, response):
        sel = Selector(response)
        str_xpath = 

    @staticmethod
    def parse_operate_mysql():
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
        # conn = pymysql.connect(config)
        # cursor = conn.cursor()
        # close
        # ('select * from call_bid')

