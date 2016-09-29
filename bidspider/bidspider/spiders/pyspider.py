# import os
# import re
import scrapy
# import urllib2

from scrapy.selector import Selector
from bidspider.items import BidspiderItem
# from scrapy.http import Request

class bidSpider(scrapy.Spider):
    name                = "BidSpider"
    allowed_domains     = ["www.chinabidding.com.cn"]
    start_urls          = ["https://www.chinabidding.cn/search/searchzbw/search2?keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&table_type=&areaid=&categoryid=1&b_date=year",
                           "https://www.chinabidding.cn/search/searchzbw/search2?rp=22&categoryid=1&keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&page=2&areaid=&table_type=0&b_date=year"]

    def parse(self, response):
        sel             = Selector(response)
        strXpathPre     = '//*[@id="cTable"]/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr['
        strXpathEx      = ']/td[2]/a/'
        BEGINORDER      = 2
        ENDORDER        = 44
        items           = []
        filetag         = open('x.txt','w')
        while BEGINORDER <= ENDORDER:
            item                 = BidspiderItem()
            strXpath             = strXpathPre + str(BEGINORDER) + strXpathEx
            urlTrans             = sel.xpath( strXpath + '@href' ).extract()
            titleTrans           = sel.xpath( strXpath + 'text()' ).extract()
            item['sigUrl']       = 'www.chinabidding.cn/' + urlTrans[0].encode('utf-8')
            item['bidTitle']     = titleTrans[0]
            BEGINORDER += 2
            items.append(item)

        for i in items:
            filetag.write(i['bidTitle'].encode('utf-8') + ',')
            filetag.write(i['sigUrl'].encode('utf-8') + '\n')

        filetag.close()
        # filetag.write(items)

        '''
        https://www.chinabidding.cn/search/searchzbw/search2?keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&table_type=&areaid=&categoryid=1&b_date=year
        https://www.chinabidding.cn/search/searchzbw/search2?rp=22&categoryid=1&keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&page=2&areaid=&table_type=0&b_date=year
        https://www.chinabidding.cn/search/searchzbw/search2?rp=22&categoryid=1&keywords=%E5%9F%8E%E5%B8%82%E8%BD%A8%E9%81%93&page=3&areaid=&table_type=0&b_date=year
        '''
    # def parse_


