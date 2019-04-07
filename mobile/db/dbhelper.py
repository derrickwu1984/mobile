# _*_coding:utf-8_*_
__author__ = 'wmx'
__date__ = '2019/4/4 9:44'

import  pymysql,uuid,logging,copy
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings #导入setting文件


class DBHelper():

    def __init__(self):
        settings = get_project_settings()

        dbparam = dict (
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',#编码要加上，否则可能出现中文乱码问题
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = False,
        )
        # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql',**dbparam)
        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    #插入数据
    def insert_billInfo(self,item):
        insert_sql = """
        insert into mobile_custInfo(object_id,crawldate,userid,rangeno,phoneno,querymonth,
                                  acctflag,paytype,debtfee,fixtype,
                                  payname,prodname,fee,openflag,
                                  custbrand,actualbal,custlocation,creditbal,
                                  totalfee,actualfee,marketing)
                       values (%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,
                                %s,%s,%s,%s,
                                %s,%s,%s,%s,
                                %s,%s,%s,%s)
            """
        # 对象拷贝   深拷贝
        asynItem = copy.deepcopy(item)
        # 调用插入的方法
        query = self.dbpool.runInteraction(self._billInfo_insert,insert_sql,asynItem)
        # 调用异常处理方法
        query.addErrback(self._handle_error)
        return item

    # 写入数据库中
    def _billInfo_insert(self,canshu,sql,item):
        # 取出要存入的数据，这里item就是爬虫代码爬下来要存入items内的数据
        params = (str(uuid.uuid1()),item["crawldate"],item["userid"], item["rangeno"], item["phoneno"], item["querymonth"]
                                    , item["acctflag"], item["paytype"], item["debtfee"], item["fixtype"]
                                    , item["payname"], item["prodname"], item["fee"], item["openflag"]
                                    , item["custbrand"], item["actualbal"], item["custlocation"], item["creditbal"]
                                    , item["totalfee"], item["actualfee"],"O")
        canshu.execute(sql, params)

    def insert_discount(self,item):
        insert_sql = """
        insert into mobile_discountInfo(object_id,crawldate,phoneNo,startdate,
                                        enddate,discntcode,productid,discntname)
                       values (%s,%s,%s,%s,
                                %s,%s,%s,%s)
            """
        # 对象拷贝   深拷贝
        asynItem = copy.deepcopy(item)
        # 调用插入的方法
        query = self.dbpool.runInteraction(self._discountInfo_insert,insert_sql,asynItem)
        # 调用异常处理方法
        query.addErrback(self._handle_error)
        return item


    def _discountInfo_insert(self,canshu,sql,item):
        # 取出要存入的数据，这里item就是爬虫代码爬下来要存入items内的数据
        params = (str(uuid.uuid1()),item["crawldate"],item["phoneNo"],
                  item["startdate"],item["enddate"], item["discntcode"],
                  item["productid"],item["discntname"])
        canshu.execute(sql, params)

    def insert_buyphone(self,item):
        insert_sql = """
        insert into mobile_buyphoneInfo(object_id,crawldate,phoneNo,startdate,
                                        enddate,bindsaleattr,imei,foregift,
                                        devicebrand,devicename,saledesc,devicetype,
                                        feeitemcode,saleprice,mpfee)
                       values (%s,%s,%s,%s,
                                %s,%s,%s,%s,
                                %s,%s,%s,%s,
                                %s,%s,%s)
            """
        # 对象拷贝   深拷贝
        asynItem = copy.deepcopy(item)
        # 调用插入的方法
        query = self.dbpool.runInteraction(self._buyphoneInfo_insert,insert_sql,asynItem)
        # 调用异常处理方法
        query.addErrback(self._handle_error)
        return item

    def _buyphoneInfo_insert(self,canshu,sql,item):
        # 取出要存入的数据，这里item就是爬虫代码爬下来要存入items内的数据
        params = (str(uuid.uuid1()),item["crawldate"],item["phoneNo"],
                  item["startdate"],item["enddate"], item["bindsaleattr"],
                  item["imei"], item["foregift"], item["devicebrand"],
                  item["devicename"], item["saledesc"], item["devicetype"],
                  item["feeitemcode"],item["saleprice"],item["mpfee"])
        canshu.execute(sql, params)


    def _handle_error(self,failure):
        logging.warning("--------------database operation exception!!----------------")
        logging.warning(failure)