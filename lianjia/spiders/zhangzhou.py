# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 19:38:44 2016

@author: Dee
"""

import scrapy
import datetime
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re
from scrapy import Request
from lianjia.items import LoupanItem, XiaoquBaseItem, XiaoquItem, HouseItem, OrderItem, XiaoquPriceItem
from lianjia.pipelines import HZloupanPipeline, HZxiaoquPipeline, HZorderPipeline



class HangZhouLouPanSpider(scrapy.spiders.Spider):
    download_delay = 1
    pipeline = set([HZloupanPipeline])
    name = "hzloupan"
    allowed_domains = ['hz.lianjia.com', 'hz.fang.lianjia.com']
    start_urls = [
        "http://hz.fang.lianjia.com/loupan/"
    ]

    def parse(self, response):
        print(response.url)
        lis = response.xpath('//ul[@id="house-lst"]/li')
        for li in lis:
            item = LoupanItem()
            item['url'] = "http://hz.fang.lianjia.com/loupan" + \
                li.xpath('.//a[1]/@href').extract_first()
            item['name'] = li.xpath('.//a[1]/text()').extract_first()
            item['region'] = li.xpath('.//span[@class="region"]/text()').extract_first()
            area = li.xpath('.//div[@class="area"]/span/text()').extract()
            if len(area) >=1:
                item['area'] = area[0]
            item['layout'] = li.xpath('.//div[@class="area"]/text()').extract_first().strip()
            item['other_tag'] = li.xpath('.//div[@class="other"]/span/text()').extract()
            item['on_sold'] = li.xpath('.//span[@class="onsold"]/text()').extract_first()
            item['house_type'] = li.xpath('.//span[@class="live"]/text()').extract_first()
            price_type = li.xpath('.//div[@class="average"]/text()').extract()
            price_type = [i.strip() for i in price_type]
            if price_type:
                item['price_type'] = price_type[0]
            if len(price_type) >= 2:
                item['price_measure'] = price_type[1]
            item['price_num'] = li.xpath('.//div[@class="average"]/span/text()').extract_first()
            item['create_time'] = datetime.datetime.now()
            yield item
        
        # page_list
        page_url = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()
        page_num = response.xpath('//div[@class="page-box house-lst-page-box"]').re(r'(?<=totalPage":)\d+')
        if page_num:
            for i in range(2,int(page_num[0]) + 1):
                url = 'http://hz.fang.lianjia.com' + page_url.format(page=i)
                yield Request(url, callback=self.parse)
            
        
class HangZhouXiaoQuSpider(scrapy.spiders.Spider):
    download_delay = 1 
    pipeline = set([HZxiaoquPipeline])
    name = 'hzxiaoqu'
    allowed_domains = ['hz.lianjia.com', 'hz.fang.lianjia.com']
    start_urls = [
        "http://hz.lianjia.com/xiaoqu/"
    ]
    
    def parse(self, response):
        position_list = response.xpath('//div[@data-role="ershoufang"]/div[1]/a/@href').extract()
        position_list = ["http://hz.lianjia.com" + i for i in position_list]
        print(position_list)

        for url in position_list:
            yield Request(url, callback=self.parse_item_base)


    def parse_item_base(self, response):
        '''
        列表中小区基本信息
        '''
        print('XQ_BASE:',response.url)
        lis = response.xpath('//ul[@class="listContent"]/li[@class="clear"]')
        for li in lis:
            item = XiaoquBaseItem()
            
            item['name'] = li.xpath('.//div[@class="title"]/a/text()').extract_first()
            item['url'] = li.xpath('.//div[@class="title"]/a/@href').extract_first()
            if item['url']:
                xq_id = re.search(r'(?<=xiaoqu/)\d+', item['url'])
                if xq_id:
                    item['xq_id'] = xq_id.group()
            item['strike'] = li.xpath('.//div[@class="houseInfo"]/a[1]/text()').extract_first()
            item['hire'] = li.xpath('.//div[@class="houseInfo"]/a[2]/text()').extract_first()
            item['district'] = li.xpath('.//div[@class="positionInfo"]/a/text()').extract()
            item['price'] = li.xpath('.//div[@class="totalPrice"]/span/text()').extract_first()
            item['on_sell_count'] = li.xpath('.//div[@class="sellCount"]/a/span/text()').extract_first()
            item['on_sell_url'] = li.xpath('.//div[@class="sellCount"]/a/@href').extract_first()
            item['create_time'] = datetime.datetime.now()
            yield item
        
        # 小区详细信息
        for li in lis:
            url = li.xpath('.//div[@class="title"]/a/@href').extract_first()
            if url:
                yield Request(url, callback=self.parse_item_info)
        
        # page_list
        page_url = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()
        page_num = response.xpath('//div[@class="page-box house-lst-page-box"]').re(r'(?<=totalPage":)\d+')
        print('PAGE_LIST',response.url, page_num)
        if page_num:
            for i in range(2,int(page_num[0]) + 1):
                url = 'http://hz.lianjia.com' + page_url.format(page=i)
                yield Request(url, callback=self.parse_item_base)
        
    def parse_item_info(self, response):
        '''
        小区详细信息
        '''
        print('XQ_INFO:',response.url)
        item = XiaoquItem()
        xq_id = re.search(r'(?<=xiaoqu/)\d+', response.url)
        if xq_id:
            item['xq_id'] = xq_id.group()
        item['url'] = response.url
        item['name'] = response.xpath('//h1[@class="detailTitle"]/text()').extract_first()
        item['average_price'] = response.xpath('//span[@class="xiaoquUnitPrice"]/text()').extract_first()
        xiaoqu_info = response.xpath('//span[@class="xiaoquInfoContent"]/text()').extract()
        if len(xiaoqu_info) >= 8:
            item['build_year'] = xiaoqu_info[0]
            item['build_type'] = xiaoqu_info[1]
            item['manage_fee'] = xiaoqu_info[2]
            item['manage_campany'] = xiaoqu_info[3]
            item['dev_campany'] = xiaoqu_info[4]
            plot_ratio = re.search(r'(?<=容积率/)\d*\.*\d*',xiaoqu_info[5])
            if plot_ratio:
                item['plot_ratio'] = plot_ratio.group()
            green_ratio = re.search(r'(?<=绿化率/)\d*%',xiaoqu_info[5])
            if green_ratio:
                item['green_ratio'] = green_ratio.group()
            item['building_num'] = xiaoqu_info[6]
            item['house_num'] = xiaoqu_info[7]
        item['order_url'] = response.xpath('//div[@class="frameDeal"]/a/@href').extract_first()
        item['create_time'] = datetime.datetime.now()
        yield item
        
        # 小区平均参考价
        xq_id = re.search(r'(?<=xiaoqu/)\d+', response.url)
        if xq_id:
            xq_id = xq_id.group()
            xq_price_url = 'http://hz.lianjia.com/fangjia/priceTrend/c' + xq_id
            yield Request(xq_price_url, callback=self.parse_item_price)
    
    
    def parse_item_price(self, response):
        '''
        小区参考价格
        '''
        print('PRICE:' ,response.url)
        item = XiaoquPriceItem()
        item['url'] = response.url
        xq_id = re.search(r'(?<=priceTrend/c)\d+', response.url)
        if xq_id:
            item['xq_id'] = xq_id.group()
        json_str = response.body.decode('utf-8')
        json_dict = json.loads(json_str)
        time = json_dict['time']['year'] + json_dict['time']['month'] +json_dict['time']['day']
        item['time'] = time 
        item['create_time'] = datetime.datetime.now()
        if 'currentLevel' in json_dict:
            month_list = json_dict['currentLevel']['month']
            avg_price_list = json_dict['currentLevel']['dealPrice']['total']
            avg_price = dict(zip(month_list,avg_price_list))
            item['avg_price'] = avg_price
        if 'upLevel' in json_dict:
            month_list = json_dict['upLevel']['month']
            region_avg_price_list = json_dict['upLevel']['dealPrice']['total']
            region_avg_price = dict(zip(month_list, region_avg_price_list))
            item['region_avg_price'] = region_avg_price
        item['create_time'] = datetime.datetime.now()
        yield item
        


class HangZhouChengJiaoSpider(scrapy.spiders.Spider):
    download_delay = 1
    pipeline = set([HZorderPipeline])
    name = "hzchengjiao"
    allowed_domains = ['hz.lianjia.com', 'hz.fang.lianjia.com']
    start_urls = [
        "http://hz.lianjia.com/chengjiao/"
    ]

    def parse(self, response):
        position_list = response.xpath('//div[@data-role="ershoufang"]/div[1]/a/@href').extract()
        position_list = ["http://hz.lianjia.com" + i for i in position_list]
        print(position_list)

        for url in position_list:
            yield Request(url, callback=self.parse_item_order)    
    
    def parse_item_order(self, response):
        '''
        成交记录
        '''
        print(response.url)
        lis = response.xpath('//ul[@class="listContent"]/li')
        for li in lis:
            item = OrderItem()
            title = li.xpath('.//div[@class="title"]/a/text()').extract_first()
            if title:
                title = title.strip().split()
                item['xq_name'] = title[0]
                item['style'] = title[1]
                item['area'] = title[2]
            item['url'] = li.xpath('.//div[@class="title"]/a/@href').extract_first()
            item['direction'] = li.xpath('.//div[@class="houseInfo"]/text()').extract_first()
            item['sign_time'] = li.xpath('.//div[@class="dealDate"]/text()').extract_first()
            item['total_price'] = li.xpath('.//div[@class="totalPrice"]/span/text()').extract_first()
            position_info = li.xpath('.//div[@class="positionInfo"]/text()').extract_first()
            if position_info:
                position_info = position_info.strip().split()
                item['floor'] = position_info[0]
                if len(position_info) >= 2:
                    item['build_year'] = position_info[1]
            item['unit_price'] = li.xpath('.//div[@class="unitPrice"]/span/text()').extract_first()
            other = li.xpath('.//div[@class="positionInfo"]/text()').extract()
            item['create_time'] = datetime.datetime.now()
            if other:
                for i in other:
                    if i.find('满') == 0:
                        item['house_class'] = i
                    elif i.find('距') == 0:
                        item['subway'] = i
                    elif re.search(r'小|中|高|学', i):
                        item['school'] = i
            yield item
            
        # page_list
        page_url = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()
        page_num = response.xpath('//div[@class="page-box house-lst-page-box"]').re(r'(?<=totalPage":)\d+')
        if page_num:
            for i in range(2,int(page_num[0]) + 1):
                url = 'http://hz.lianjia.com' + page_url.format(page=i)
                yield Request(url, callback=self.parse_item_order)
            