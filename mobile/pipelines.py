# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid,pymysql,logging

from .items import MobileItem,DicountItem

from mobile.db.dbhelper import DBHelper
class MobilePipeline(object):
    def __init__(self):
        # self.conn = pymysql.connect('WIN-EGP38V915TC', 'root', 'root12#$', 'website', charset='utf8', use_unicode=True)
        # self.conn = pymysql.connect('localhost', 'root', 'root12#$', 'website', charset='utf8', use_unicode=True)
        # self.curor = self.conn.cursor()
        # pass
        self.db = DBHelper()
    def process_item(self, item, spider):
        if (len(item) > 2 and  item.__class__ == MobileItem):
            logging.warning("MobileItem")
            self.db.insert_billInfo(item)
        elif (len(item) > 2 and item.__class__ == DicountItem):
            logging.warning("DicountItem")
            self.db.insert_discount(item)
        return item

class DiscountPipeline(object):
    def __init__(self):
        self.db = DBHelper()
    def process_item(self, item, spider):
        if len(item) > 2:
            self.db.insert_discount(item)
        return item
