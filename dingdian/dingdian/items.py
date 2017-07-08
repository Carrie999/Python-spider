# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    #小说名字
    author = scrapy.Field()
    #作者
    novelurl = scrapy.Field()
    #小说地址
    serialstatus = scrapy.Field()
    #小说状态
    serialnumber = scrapy.Field()
    #连载字数
    category = scrapy.Field()
    #小说编号
    name_id = scrapy.Field()