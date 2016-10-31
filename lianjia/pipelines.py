# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



from lianjia.storemongo import db
import functools
import logging
from lianjia.items import LoupanItem, XiaoquBaseItem, XiaoquItem, HouseItem, OrderItem, XiaoquPriceItem


def check_spider_pipeline(process_item_method):

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        msg = "{status} {name} pipeline step"
        
        if self.__class__ in spider.pipeline:
            logging.info(msg.format(name=self.__class__.__name__, status="executing"))
            return process_item_method(self, item, spider)

        else:
            logging.info(msg.format(name=self.__class__.__name__, status="skipping"))
            return item

    return wrapper

class LianjiaPipeline(object):    
    def process_item(self, item, spider):
        return item
        

class HZloupanPipeline(object):
    '''
    楼盘数据
    '''
    def open_spider(self, spider):
        self.loupan = db.hangzhouloupan
    
    @check_spider_pipeline
    def process_item(self, item, spider):
        try:
            self.loupan.insert_one(dict(item))
        except Exception as e:
            print(e)
        return item


class HZxiaoquPipeline(object):
    '''
    小区数据
    '''
    def open_spider(self, spider):
        self.xiaoqu_base = db.hzxq_base
        self.xiaoqu = db.hangzhouxiaoqu
        self.xiaoqu_price = db.hzxq_price
    
    @check_spider_pipeline
    def process_item(self, item, spider):
        try:
            if isinstance(item, XiaoquBaseItem):
                self.xiaoqu_base.insert_one(dict(item))
            elif isinstance(item, XiaoquItem):
                self.xiaoqu.insert_one(dict(item))
            elif isinstance(item, XiaoquPriceItem):
                self.xiaoqu_price.insert_one(dict(item))
        except Exception as e:
            print(e)
        return item 

class HZorderPipeline(object):
    '''
    成交数据
    '''
    def open_spider(self, spider):
        self.order = db.hangzhou_order
    
    @check_spider_pipeline
    def process_item(self, item, spider):
        try:
            if isinstance(item, OrderItem):
                self.order.insert_one(dict(item))
        except Exception as e:
            print(e)
        return item        
    
class HZhousePipeline(object):
    '''
    在售二手房数据
    '''
    def open_spider(self, spider):
        self.house = db.hangzhouhouse
    
    @check_spider_pipeline
    def process_item(self, item, spider):
        try:
            if isinstance(item, HouseItem):
                self.house.insert_one(dict(item))
        except Exception as e:
            print(e)
        return item        
