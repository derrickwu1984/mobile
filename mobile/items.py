# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MobileItem(scrapy.Item):
    # define the fields for your item here like:
    crawldate = scrapy.Field()
    rangeno = scrapy.Field()
    phoneno = scrapy.Field()
    querymonth = scrapy.Field()
    acctflag = scrapy.Field()
    paytype = scrapy.Field()
    debtfee = scrapy.Field()
    fixtype = scrapy.Field()
    payname = scrapy.Field()
    prodname = scrapy.Field()
    fee = scrapy.Field()
    openflag = scrapy.Field()
    custbrand = scrapy.Field()
    actualbal = scrapy.Field()
    custlocation = scrapy.Field()
    creditbal = scrapy.Field()
    totalfee = scrapy.Field()
    actualfee = scrapy.Field()



    pass
