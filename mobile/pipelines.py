# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb,uuid

class MobilePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('192.168.1.105', 'root', 'root12#$', 'website', charset='utf8', use_unicode=True)
        self.curor = self.conn.cursor()
        pass

    def process_item(self, item, spider):
        insert_sql = """
        insert into mobile_custInfo(object_id,crawldate,rangeno,phoneno,querymonth,
                                  acctflag,paytype,debtfee,fixtype,
                                  payname,prodname,fee,openflag,
                                  custbrand,actualbal,custlocation,creditbal,
                                  totalfee,actualfee)
                       values (%s,%s,%s,%s,
                                %s,%s,%s,%s,
                                %s,%s,%s,%s,
                                %s,%s,%s,%s,
                                %s,%s,%s)
            """
        if len(item) > 2:
                self.curor.execute(insert_sql,
                                  (str(uuid.uuid1()),item["crawldate"], item["rangeno"], item["phoneno"], item["querymonth"]
                                    , item["acctflag"], item["paytype"], item["debtfee"], item["fixtype"]
                                    , item["payname"], item["prodname"], item["fee"], item["openflag"]
                                    , item["custbrand"], item["actualbal"], item["custlocation"], item["creditbal"]
                                    , item["totalfee"], item["actualfee"]))
                self.conn.commit()


        return item
