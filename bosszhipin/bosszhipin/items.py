# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BosszhipinItem(scrapy.Item):

    # 职位名称
    name = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 地址
    message = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 公司连接
    company_href = scrapy.Field()
    # 职位描述
    requirement = scrapy.Field()
