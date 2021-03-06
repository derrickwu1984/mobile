# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MobileItem(scrapy.Item):
    # define the fields for your item here like:
    crawldate = scrapy.Field()
    userid = scrapy.Field()
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

# 优惠信息
class DicountItem(scrapy.Item):
    crawldate = scrapy.Field()
    phoneNo = scrapy.Field()
    startdate = scrapy.Field()
    enddate = scrapy.Field()
    discntcode = scrapy.Field()
    productid = scrapy.Field()
    discntname = scrapy.Field()


class BuyphoneItem(scrapy.Item):
    crawldate = scrapy.Field()
    phoneNo = scrapy.Field()
    startdate = scrapy.Field()
    enddate = scrapy.Field()
    bindsaleattr = scrapy.Field()
    imei = scrapy.Field()
    foregift = scrapy.Field()
    devicebrand = scrapy.Field()
    devicename = scrapy.Field()
    saledesc = scrapy.Field()
    devicetype = scrapy.Field()
    feeitemcode = scrapy.Field()
    saleprice = scrapy.Field()
    mpfee = scrapy.Field()
