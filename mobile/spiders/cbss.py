# -*- coding: utf-8 -*-
import scrapy,logging,requests,time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from scrapy.http import Request
from urllib import parse
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #期望的条件
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.loader import  ItemLoader
from mobile.items import MobileItem,DicountItem,BuyphoneItem
import time,re
import json
import datetime
import pickle
import sys
from io import BytesIO
from scrapy.http.cookies import CookieJar

# set default logging configuration
# logger = logging.getLogger()  # initialize logging class
# logger.setLevel(logging.WARNING)  # default log level
# format = logging.Formatter("%(asctime)s - %(message)s")  # output format
# sh = logging.StreamHandler(stream=sys.stdout)  # output to standard output
# sh.setFormatter(format)
# logger.addHandler(sh)
class CbssSpider(scrapy.Spider):
    name = 'cbss'
    allowed_domains = ['cbss.10010.com']
    start_urls = ['https://cbss.10010.com/essframe']
    login_url = "https://cbss.10010.com/essframe"
    # 登陆后的链接
    initmy_url = "https://bj.cbss.10010.com/essframe"
    post_url="https://bj.cbss.10010.com/acctmanm;"
    post_discount_url = "https://bj.cbss.10010.com/custserv?service=swallow/personalserv.integratequerytrade.IntegrateQueryTrade/queryTabInfo/1"
    driver_path="D:/tools/IEDriverServer.exe"
    # driver_path = "Z:/tools/IEDriverServer.exe"
    # driver_path = "C:/IEDriverServer.exe"
    userName="bjsc-wangj1"
    passWd="BySh@2019"
    province_code = "bj"
    depart_id="11b2pk1"
    province_id="11"
    driver = webdriver.Ie(driver_path)
    js_exec="var but_click=document.getElementsByClassName('submit')[0].children[0].onclick"



    def __init__(self,rangeNo,startNo,endNo):
        self.rangeNo=rangeNo
        self.startNo=startNo
        self.endNo=endNo
        self.cur_month = self.date_Formate(datetime.datetime.now().month)
        self.cur_day =self.date_Formate(datetime.datetime.now().day)
        self.crawldate = str(datetime.datetime.now().year) + self.cur_month + self.cur_day
        pass
    # 将月份、日期小于10的前面补充0
    def date_Formate(self,object):
        if (object<10):
            object="0"+str(object)
        return object
    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)
    #     登录逻辑
    def login(self, response):
        self.driver.get(self.login_url)
        time.sleep(3)
        self.driver.find_element_by_id("STAFF_ID").send_keys(self.userName)
        self.driver.find_element_by_id("LOGIN_PASSWORD").send_keys(self.passWd)
        Select(self.driver.find_element_by_name("LOGIN_PROVINCE_CODE")).select_by_value(self.province_id)
        # captha_input=input(u"请输入验证码:")
        # VERIFY_CODE_ELE = driver.find_element_by_id("VERIFY_CODE")
        # VERIFY_CODE_ELE.send_keys(captha_input)
        WebDriverWait(self.driver, 1000).until(EC.url_to_be(self.initmy_url))
        logging.warning("恭喜您，您已登录成功了！")
        # 如果没有使用此行代码，则无法找到页面frame中的任何页面元素
        WebDriverWait(self.driver, 600).until(EC.presence_of_element_located((By.ID, 'navframe')))
        self.driver.switch_to.frame("navframe")
        # time.sleep(30)
        WebDriverWait(self.driver, 600).until(EC.presence_of_element_located((By.ID,'SECOND_MENU_LINK_BIL6500')))
        # in order to find CSM1001
        js_query_acct="var query_acct=document.getElementById('SECOND_MENU_LINK_BIL6500').onclick()"
        self.driver.execute_script(js_query_acct)
        time.sleep(3)
        # WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.ID, 'CSM1001')))
        WebDriverWait(self.driver, 600).until(EC.presence_of_element_located((By.ID, 'BIL6531')))
        openmenu = self.driver.find_element_by_id("BIL6531").get_attribute("onclick")
        r = re.findall(r"'([\S\s]+?)'", openmenu)
        request_url="https://"+self.province_code+".cbss.10010.com"+r[0]+"&staffId="+self.userName+"&departId="+self.depart_id+"&subSysCode=CBS&eparchyCode=0010"
        logging.warning(request_url)
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        cookies_dict = {}
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        with open('cookies.txt', 'w+') as f:
            json.dump(cookies_dict, f)
        with open('cookies.txt', 'r') as f:
            cookie_out = json.load(f)
        headers = {
            'referer': 'https://bj.cbss.10010.com/essframe?service=page/component.Navigation&listener=init&needNotify=true&staffId='+self.userName+'&departId='+self.depart_id+'&subSysCode=CBS&eparchyCode=0010',
            'Host':'bj.cbss.10010.com'
        }
        yield scrapy.Request(request_url,headers=headers,cookies=cookie_out,callback=self.parse_rangeNo,meta={'reqeust_url':request_url})
    # 实时/月结账单查询 报文格式
    def prepare_data(self,eparchy_code,query_month,phoneNo,cond_NET_TYPE_CODE,cond_PARENT_TYPE_CODE,cond_ROUTE_EPARCHY_CODE,Form0,service):
        data={
            "back_ACCT_ID":"",
            "back_USER_ID":"",
            "bquerytop":"+%B2%E9+%D1%AF+",
            "cond_ACCT_ID":"",
            "cond_BILLSEARCH_FLAG":"0",
            "cond_CBSSREQUEST_SOURCE":"",
            "cond_CONFIG_BILLCOUNT":"800",
            "cond_CYCLE_ID":query_month,
            "cond_CYCLE_SEGMENT":"6",
            "cond_END_CYCLE_ID":query_month,
            "cond_ID_TYPE":"1",
            "cond_NET_TYPE_CODE":"50",
            "cond_NODISTURB":"",
            "cond_PARENT_TYPE_CODE":"0",
            "cond_PRE_TAG":"0",
            "cond_REMOVE_TAG":"0",
            "cond_ROUTE_EPARCHY_CODE":eparchy_code,
            "cond_SEND_SN":phoneNo,
            "cond_SENDBILLSMS_RIGHT":"0",
            "cond_SERIAL_NUMBER":phoneNo,
            "cond_SMS":"",
            "cond_USER_ID":"",
            "cond_USER_SERVICE_CODE":"0",
            "cond_WRITEOFF_MODE":"1",
            "cond_X_USER_COUNT":"",
            "Form0":Form0,
            "MULTI_ACCT_DATA":"",
            "NOTE_ITEM_DISPLAY":"",
            "service":service,
            "smsFlag":"false",
            "sp":"S0",
            "userinfoback_USER_ID":"",
            "X_CODING_STR":""
        }
        return data
    # 实时/月结账单查询 号段遍历
    def parse_rangeNo(self,response):
        reqeust_url=response.meta['reqeust_url']
        html=etree.HTML(response.body.decode("gbk"))
        time.sleep(10)
        BSS_ACCTMANM_JSESSIONID=html.xpath('//form/@action')[0].split(";")[1]
        service=html.xpath('//input[@name="service"]/@value')[0]
        Form0=html.xpath('//input[@name="Form0"]/@value')[0]
        yy=datetime.datetime.now().year
        mm=datetime.datetime.now().month
        if (mm<10 and mm>1):
            mm="0"+str(mm-1)
        if (mm==1):
            yy=yy-1
            mm=12
        query_month=str(yy)+str(mm)
        # #bulid post method
        post_url=self.post_url+BSS_ACCTMANM_JSESSIONID
        headNo = self.rangeNo
        # for subNo in range(8800,8899):
        for subNo in range(int(self.startNo), int(self.endNo)):
            phoneNo=headNo+str(subNo).zfill(4)
            cond_NET_TYPE_CODE=''
            cond_PARENT_TYPE_CODE=''
            cond_ROUTE_EPARCHY_CODE='0010'
            data=self.prepare_data(cond_ROUTE_EPARCHY_CODE,query_month,phoneNo,cond_NET_TYPE_CODE,cond_PARENT_TYPE_CODE,cond_ROUTE_EPARCHY_CODE,Form0,service)
            BSS_ACCTMANM_JSESSIONID_array=BSS_ACCTMANM_JSESSIONID.split("=")
            BSS_ACCTMANM_JSESSIONID_key=BSS_ACCTMANM_JSESSIONID_array[0]
            BSS_ACCTMANM_JSESSIONID_value = BSS_ACCTMANM_JSESSIONID_array[1]
            BSS_ACCTMANM_JSESSIONID_dict={BSS_ACCTMANM_JSESSIONID_key:BSS_ACCTMANM_JSESSIONID_value}
            with open('cookies.txt', 'r') as f:
                cookie_billPage = json.load(f)
            cookie_billPage.update(BSS_ACCTMANM_JSESSIONID_dict)
            post_headers = {
                'referer':reqeust_url,
                'Host':'bj.cbss.10010.com',
            }
            # time.sleep(3)
            # 查询月账单信息
            yield scrapy.FormRequest(url=post_url, formdata=data, method="POST",cookies=cookie_billPage, callback=self.parse_monthly_bill,meta={'phoneNo':phoneNo,"headNo":headNo,"query_month":query_month})
    # 获取cookie
    def get_cookie(self):
        cookies_dict = {}
        # cookies = self.driver.get_cookies()
        # for cookie in cookies:
        #     cookies_dict[cookie['name']] = cookie['value']
        # with open('cookies.txt', 'w+') as f:
        #     json.dump(cookies_dict, f)
        with open('cookies.txt', 'r') as f:
            cookie_out = json.load(f)
        return cookie_out
    # 获取headers
    def get_headers(self):
        headers = {
            'referer': 'https://bj.cbss.10010.com/essframe?service=page/component.Navigation&listener=init&needNotify=true&staffId='+self.userName+'&departId='+self.depart_id+'&subSysCode=CBS&eparchyCode=0010',
            'Host':'bj.cbss.10010.com'
        }
        return headers
    def query_integrated_information(self,response):
        html = etree.HTML(response.body.decode("gbk"))
        logging.warning("===========query_integrated_information==========")
        DateField=""
        _BoInfo=html.xpath('//input[@name="_BoInfo"]/@value')[0]
        ACCPROVICE_ID=html.xpath('//input[@name="ACCPROVICE_ID"]/@value')[0]
        allInfo=html.xpath('//input[@name="allInfo"]/@value')[0]
        phoneNo = response.meta['phoneNo']
        currentRightCode=html.xpath('//input[@name="currentRightCode"]/@value')[0]
        Form0 = html.xpath('//input[@name="Form0"]/@value')[0]
        PROVICE_ID= html.xpath('//input[@name="PROVICE_ID"]/@value')[0]
        queryTradehide=html.xpath('//input[@name="queryTradehide"]/@value')[0]
        service=html.xpath('//input[@name="service"]/@value')[0]
        tabSetList=html.xpath('//input[@name="tabSetList"]/@value')[0]
        dataForm=self.custserv_dataForm(DateField,_BoInfo,ACCPROVICE_ID,allInfo,phoneNo,ACCPROVICE_ID,currentRightCode,Form0,PROVICE_ID,queryTradehide,service,tabSetList)
        post_intetrated_url="https://bj.cbss.10010.com/custserv"
        yield scrapy.FormRequest(url=post_intetrated_url, formdata=dataForm, method="POST", headers=self.get_headers(),cookies=self.get_cookie(),
                                 callback=self.get_user_id,meta={'phoneNo': phoneNo},dont_filter=True)
    def get_user_id(self,response):
        logging.warning("=============get_user_id===============")
        html = etree.HTML(response.body.decode("gbk"))
        USER_ID = html.xpath('//input[@name="USER_ID"]/@value')[0]
        currentRightCode= html.xpath('//input[@name="currentRightCode"]/@value')[0]
        phoneNo = response.meta['phoneNo']
        logging.warning(phoneNo)
        # 优惠信息posturl
        dataForm=self.discount_dataForm(currentRightCode,phoneNo,USER_ID)
        post_discount_url="https://bj.cbss.10010.com/custserv?service=swallow/personalserv.integratequerytrade.IntegrateQueryTrade/queryTabInfo/1"
        # yield scrapy.FormRequest(url=post_discount_url, formdata=dataForm, method="POST", headers=self.get_headers(),cookies=self.get_cookie(),
        #                          callback=self.parse_discount_info,meta={'phoneNo': phoneNo},dont_filter=True)

    def get_discount_info(self,response):
        logging.warning("============get_discount_info============")
        phoneNo = response.meta['phoneNo']
        response_str = response.body.decode()
        logging.warning(phoneNo)
        html = bytes(bytearray(response_str, encoding='utf-8'))
        html = etree.HTML(html)
        nodes = html.xpath("//data")
        for node in nodes:
            discountItemLoader = ItemLoader(item=DicountItem(),response=response)
            discountItemLoader.add_value("crawldate", self.crawldate)
            discountItemLoader.add_value("phoneNo", phoneNo)
            discountItemLoader.add_value("startdate", node.attrib['startdate'])
            discountItemLoader.add_value("enddate", node.attrib['enddate'])
            discountItemLoader.add_value("discntcode", node.attrib['discntcode'])
            discountItemLoader.add_value("productid", node.attrib['productid'])
            discountItemLoader.add_value("discntname", node.attrib['discntname'])
            discountInfo = discountItemLoader.load_item()
            yield discountInfo

    def get_buy_phone_info(self,response):
        logging.warning("============get_buy_phone_info============")
        phoneNo = response.meta['phoneNo']
        response_str = response.body.decode()
        logging.warning(response_str)
        logging.warning(phoneNo)
        html = bytes(bytearray(response_str, encoding='utf-8'))
        html = etree.HTML(html)
        nodes = html.xpath("//data")
        for node in nodes:
            buyphoneItemLoader = ItemLoader(item=BuyphoneItem(),response=response)
            buyphoneItemLoader.add_value("crawldate", self.crawldate)
            buyphoneItemLoader.add_value("phoneNo", phoneNo)
            buyphoneItemLoader.add_value("bindsaleattr", node.attrib['bindsaleattr'])
            buyphoneItemLoader.add_value("startdate", node.attrib['startdate'])
            buyphoneItemLoader.add_value("enddate", node.attrib['enddate'])
            buyphoneItemLoader.add_value("imei", node.attrib['imei'])
            buyphoneItemLoader.add_value("foregift", node.attrib['foregift'])
            buyphoneItemLoader.add_value("devicebrand", node.attrib['devicebrand'])
            buyphoneItemLoader.add_value("devicename", node.attrib['devicename'])
            buyphoneItemLoader.add_value("saledesc", node.attrib['saledesc'])
            buyphoneItemLoader.add_value("devicetype", node.attrib['devicetype'])
            buyphoneItemLoader.add_value("feeitemcode", node.attrib['feeitemcode'])
            buyphoneItemLoader.add_value("saleprice", node.attrib['saleprice'])
            buyphoneItemLoader.add_value("mpfee", node.attrib['mpfee'])
            buyphoneInfo = buyphoneItemLoader.load_item()
            yield buyphoneInfo



    # 用户资料综合查询 路径
    def get_integrated_information_url(self):
        # 查找到综合信息菜单
        # logging.warning(self.driver.page_source)
        js_query_total = "var query_acct=document.getElementById('SECOND_MENU_LINK_CSM7000').onclick()"
        self.driver.execute_script(js_query_total)
        WebDriverWait(self.driver, 6).until(EC.presence_of_element_located((By.ID, 'CSMB043')))
        clickMenuItem = self.driver.find_element_by_id("CSMB043").get_attribute("onclick")
        clickMenuItem_re = re.findall(r"'([\S\s]+?)'", clickMenuItem)
        request_url = "https://" + self.province_code + ".cbss.10010.com" + clickMenuItem_re[0] + "&staffId=" + self.userName + "&departId=" + self.depart_id + "&subSysCode=CBS&eparchyCode=0010"
        return request_url

    # 实时/月结账单查询 数据解析
    def parse_monthly_bill(self, response):
        response_str=response.body.decode("gbk")
        html = etree.HTML(response_str)
        phoneNo=response.meta['phoneNo']
        headNo =response.meta['headNo']
        query_month=response.meta['query_month']
        error_msg =""
        try:
            error_msg=html.xpath("//div[@class='tip']/ul/li/text()")[0].split("：")[0]
        except:
            pass
        if (error_msg!="" and "错误提示"==error_msg):
            logging.warning(phoneNo+"手机号未查询到或已被注销！")
        else:
            logging.warning(phoneNo+"手机号码有效！")
            userid=html.xpath('//input[@name="back_USER_ID"]/@value')[0]
            discount_dataForm = self.discount_dataForm("7","csInterquery", phoneNo, userid)
            buyphone_dataForm = self.discount_dataForm("13","csInterquery", phoneNo, userid)

            acctflag=html.xpath("//table/tr/td[2]//text()")[12].strip()
            paytype=html.xpath("//table/tr/td[2]//text()")[13].strip()
            debtfee=html.xpath("//table/tr/td[2]//text()")[14].strip()
            try:
                fixtype=html.xpath("//table/tr/td[2]//text()")[15].strip()
            except:
                fixtype=""
            payname=html.xpath("//table/tr/td[4]//text()")[-3].strip()
            prodname=html.xpath("//table/tr/td[4]//text()")[-2].strip()
            fee=html.xpath("//table/tr/td[4]//text()")[-1].strip()
            openflag=html.xpath("//table/tr/td[6]//text()")[-3].strip()
            custbrand=html.xpath("//table/tr/td[6]//text()")[-2].strip()
            actualbal=html.xpath("//table/tr/td[6]//text()")[-1].strip()
            custlocation=html.xpath("//table/tr/td[8]//text()")[0].strip()
            creditbal= html.xpath("//table/tr/td[8]//text()")[1].strip()
            totalfee = html.xpath("//table[@id='UserBillTable']//tr/td[10]//text()")[-1].strip()
            actualfee = html.xpath("//table[@id='UserBillTable']//tr/td[14]//text()")[-1].strip()

            # 数据加载到Item
            mobileItemLoader = ItemLoader(item=MobileItem(),response=response)
            mobileItemLoader.add_value("crawldate", self.crawldate)
            mobileItemLoader.add_value("userid", userid)
            mobileItemLoader.add_value("rangeno", headNo)
            mobileItemLoader.add_value("phoneno", phoneNo)
            mobileItemLoader.add_value("querymonth", query_month)
            mobileItemLoader.add_value("acctflag",acctflag)
            mobileItemLoader.add_value("paytype",paytype)
            mobileItemLoader.add_value("debtfee",debtfee)
            mobileItemLoader.add_value("fixtype",fixtype)
            mobileItemLoader.add_value("payname",payname)
            mobileItemLoader.add_value("prodname",prodname)
            mobileItemLoader.add_value("fee",fee)
            mobileItemLoader.add_value("openflag",openflag)
            mobileItemLoader.add_value("custbrand",custbrand)
            mobileItemLoader.add_value("actualbal",actualbal)
            mobileItemLoader.add_value("custlocation",custlocation)
            mobileItemLoader.add_value("creditbal",creditbal)
            mobileItemLoader.add_value("totalfee",totalfee)
            mobileItemLoader.add_value("actualfee",actualfee)
            userInfo = mobileItemLoader.load_item()
            # 账单信息
            yield userInfo
            # 优惠信息
            yield scrapy.FormRequest(url=self.post_discount_url, formdata=discount_dataForm, method="POST",headers=self.get_headers(), cookies=self.get_cookie(),
                                      callback=self.get_discount_info,meta={'phoneNo': phoneNo},dont_filter=True)
            # 购机信息
            yield scrapy.FormRequest(url=self.post_discount_url, formdata=buyphone_dataForm, method="POST",headers=self.get_headers(), cookies=self.get_cookie(),
                                      callback=self.get_buy_phone_info,meta={'phoneNo': phoneNo},dont_filter=True)

    # 报文格式
    # 用户资料综合查询
    def custserv_dataForm(self,DateField,_BoInfo,ACCPROVICE_ID,allInfo,phoneNo,proviceCode,currentRightCode,Form0,PROVICE_ID,queryTradehide,service,tabSetList):
        data={
            "$DateField": DateField,
            "_BoInfo": _BoInfo,
            "AC_INFOS": "",
            "ACCPROVICE_ID": ACCPROVICE_ID,
            "allInfo": allInfo,
            "autoSearch": "no",
            "chklistframe17_hidden": "",
            "cond_ALIASE_ACCOUNT_IN": "",
            "cond_CUST_ID": "",
            "cond_CUST_NAME": "",
            "cond_NET_TYPE_CODE": "50",
            "cond_PAGE_NUM": "",
            "cond_QUERY_METHOD": "0",
            "cond_SERIAL_NUMBER": phoneNo,
            "CS_CHR_QUERY_WO_SCORE": "0",
            "CS_CONTRAL_TAG": "0",
            "CS_SYNC_POPWINDOW": "1",
            "CUR_PROVINCE": proviceCode,
            "CURRENT_BRAND": "",
            "CURRENT_PRODUCT_NAME": "",
            "currentRightCode": currentRightCode,
            "custTreaty": "",
            "DATAFLOWTAG": "0",
            "Form0": Form0,
            "importTag": "1",
            "N2_QKWB": "",
            "N6_15906_TAGCODE": "0",
            "N6_17426_USE_TAG": "0",
            "PAY_MODE_CODE": "",
            "PROVICE_ID": PROVICE_ID,
            "QUERY_TYPE": "on",
            "queryTradehide": queryTradehide,
            "service": service,
            "sp": "S0",
            "SUPPORT_TAG": "",
            "tabSetList": tabSetList,
            "TAG_CHECKMODE_5": "",
            "TAN_CHUANG": "",
            "titleInfo": "",
            "TRADE_ID": "",
            "userAttrInfo": "",
            "VIP_CUST_LOYAL_529757_TAG": "0"
        }
        return data
    # 优惠信息查询
    def discount_dataForm(self,IDX,RIGHT_CODE,phoneNo,userId):
        data={
            "custId": "",
            "custName": "",
            "globalPageName": "personalserv.integratequerytrade.IntegrateQueryTrade",
            "IDX": IDX,
            "netTypeCode": "50",
            "passWord": "",
            "queryMethod": "0",
            "removeTag": "0",
            "resNo": "",
            "RIGHT_CODE": RIGHT_CODE,
            "serialNumber": phoneNo,
            "simCard": "null",
            "userId": userId
        }
        return data


