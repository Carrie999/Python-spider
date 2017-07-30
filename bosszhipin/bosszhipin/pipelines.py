# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import bosszhipin.settings


class BosszhipinPipeline(object):
    def process_item(self, item, spider):
        with open('zz.txt', 'a+') as f:
            f.write("{}\n".format(item))
        return item

