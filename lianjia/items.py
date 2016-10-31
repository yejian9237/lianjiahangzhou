# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LoupanItem(scrapy.Item):
    name = Field()
    url = Field()
    region = Field()
    area = Field()
    layout = Field()
    other_tag = Field()
    on_sold = Field()
    house_type = Field()
    price_num = Field()
    price_type = Field()
    price_measure = Field()
    create_time = Field()

class XiaoquBaseItem(scrapy.Item):
    xq_id = Field()
    name = Field()
    url = Field()
    strike = Field()
    hire = Field()
    district = Field()
    price = Field()
    on_sell_count = Field()
    on_sell_url = Field()
    create_time = Field()

class XiaoquItem(scrapy.Item):
    xq_id = Field()
    name = Field()
    url = Field()
    average_price = Field()
    build_year = Field()
    build_type = Field()
    manage_fee = Field()
    manage_campany = Field()
    dev_campany = Field()
    plot_ratio = Field()
    green_ratio = Field()
    building_num = Field()
    house_num = Field()
    order_url = Field()
    create_time = Field()
    
class XiaoquPriceItem(scrapy.Item):
    xq_id = Field()
    url = Field()
    time = Field()
    create_time = Field()
    avg_price = Field()
    region_avg_price = Field()
    region_name = Field()
    create_time = Field()
    

    
class OrderItem(scrapy.Item):
    url = Field()
    xq_name = Field()
    style = Field()
    area = Field()
    direction = Field()
    floor = Field()
    build_year = Field()
    sign_time = Field()
    unit_price = Field()
    total_price = Field()
    house_class = Field()
    school = Field()
    subway = Field()
    create_time = Field()
    


class HouseItem(scrapy.Item):
    pass