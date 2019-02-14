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
import time
from lxml import etree
import json
import datetime
import pickle
from PIL import Image
from io import BytesIO
from scrapy.http.cookies import CookieJar
class CbssSpider(scrapy.Spider):
    name = 'cbss'
    allowed_domains = ['cbss.10010.com']
    start_urls = ['https://cbss.10010.com/essframe']
    login_url = "https://cbss.10010.com/essframe"
    # 登陆后的链接
    initmy_url = "https://sd.cbss.10010.com/essframe"
    driver_path="D:/tools/IEDriverServer.exe"
    # driver_path = "Z:/tools/IEDriverServer.exe"
    captha_image_url="https://hq.cbss.10010.com/image?mode=validate&width=60&height=20"
    captha_image_path="Z:\\Users\\wumingxing\\Desktop\\printscreen.png"
    captha_image = "Z:\\Users\\wumingxing\\Desktop\\captha.png"
    userName=""
    passWd=""
    js_exec="var but_click=document.getElementsByClassName('submit')[0].children[0].onclick"
    # js_exec="var but_click=document.querySelector('.button')"

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)
    def login(self, response):
        driver = webdriver.Ie(self.driver_path)
        driver.get(self.login_url)
        # time.sleep(2)
        # builder=ActionChains(driver)
        # time.sleep(2)
        # driver.refresh()
        time.sleep(5)
        driver.find_element_by_id("STAFF_ID").send_keys(self.userName)
        driver.find_element_by_id("LOGIN_PASSWORD").send_keys(self.passWd)
        Select(driver.find_element_by_name("LOGIN_PROVINCE_CODE")).select_by_value("17")
        # time.sleep(2)
        # captha_input=input(u"请输入验证码:")
        # VERIFY_CODE_ELE = driver.find_element_by_id("VERIFY_CODE")
        # VERIFY_CODE_ELE.send_keys(captha_input)
        # time.sleep(2)
        logging.debug("------start------")
        WebDriverWait(driver, 1000).until(EC.url_to_be(self.initmy_url))
        logging.debug("恭喜您，您已登录成功了！")
        # 如果没有使用此行代码，则无法找到页面frame中的任何页面元素
        driver.switch_to.frame("navframe")
        time.sleep(30)
        # logging.warning("=========first==========")
        js_query_acct="var query_acct=document.getElementById('SECOND_MENU_LINK_BIL6500').onclick()"
        driver.execute_script(js_query_acct)
        time.sleep(3)
        # logging.warning("=========second==========")
        # logging.warning(driver.page_source)
        # js_query_bill = "var query_acct=document.getElementById('BIL651P').onclick()"
        # js_query_bill = "var query_acct=document.getElementById('BIL6531').onclick()"
        # driver.execute_script(js_query_bill)
        # logging.warning("=========third==========")
        CSM1001 = driver.find_element_by_id("CSM1001").get_attribute("onclick")
        CSM1001_content=CSM1001.split('&')
        LOGIN_RANDOM_CODE =CSM1001_content[3]
        LOGIN_CHECK_CODE=CSM1001_content[4]
        reqeust_url = "https://sd.cbss.10010.com/acctmanm?service=page/amarchquery.queryuserbill.QueryUserBillCBss&listener=myInitialize&RIGHT_CODE=ASMUSERTABQRY&"+LOGIN_RANDOM_CODE+"&"+LOGIN_CHECK_CODE+"&LOGIN_PROVINCE_CODE=17&IPASS_LOGIN=null&gray_staff_id=sdsc-xingyy7&gray_depart_id=17b5q7m&gray_province_code=17&gray_eparchy_code=0531&staffId=sdsc-xingyy7&departId=17b5q7m&subSysCode=CBS&eparchyCode=0531"
        # logging.warning(reqeust_url)
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        # s.keep_alive = False  # 关闭多余连接
        cookies_dict = {}
        cookies = driver.get_cookies()
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        with open('cookies.txt', 'w+') as f:
            json.dump(cookies_dict, f)
        with open('cookies.txt', 'r') as f:
            cookie_out = json.load(f)
        headers = {
            'referer': 'https://sd.cbss.10010.com/essframe?service=page/component.Navigation&listener=init&needNotify=true&staffId=sdsc-xingyy7&departId=17b5q7m&subSysCode=CBS&eparchyCode=0531',
            'Host':'sd.cbss.10010.com'
            # 'cookie': dict(cookie_out)
        }
        response_str=s.get(reqeust_url,headers=headers,cookies=cookie_out,verify= False)
        time.sleep(5)
        html=etree.HTML(response_str.content.decode('gbk'))
        time.sleep(10)
        # logging.warning(response_str.content.decode('gbk'))
        BSS_ACCTMANM_JSESSIONID=html.xpath('//form/@action')[0].split(";")[1]
        service=html.xpath('//input[@name="service"]/@value')[0]
        Form0=html.xpath('//input[@name="Form0"]/@value')[0]
        # logging.warning(html)
        # logging.warning(BSS_ACCTMANM_JSESSIONID)
        # logging.warning(service)
        # logging.warning(Form0)
        yy=datetime.datetime.now().year
        mm=datetime.datetime.now().month
        if (mm<10 and mm>1):
            mm="0"+str(mm-1)
        if (mm==1):
            yy=yy-1
            mm=12
        query_month=str(yy)+str(mm)
        #bulid post method
        post_url="https://sd.cbss.10010.com/acctmanm;"+BSS_ACCTMANM_JSESSIONID
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
            "cond_ROUTE_EPARCHY_CODE":"0531",
            "cond_SEND_SN":"13001711000",
            "cond_SENDBILLSMS_RIGHT":"0",
            "cond_SERIAL_NUMBER":"13001711000",
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
        post_headers = {
            'referer':reqeust_url,
            'Host':'sd.cbss.10010.com',
            # 'cookie': cookie_out
        }
        BSS_ACCTMANM_JSESSIONID_array=BSS_ACCTMANM_JSESSIONID.split("=")
        BSS_ACCTMANM_JSESSIONID_key=BSS_ACCTMANM_JSESSIONID_array[0]
        BSS_ACCTMANM_JSESSIONID_value = BSS_ACCTMANM_JSESSIONID_array[1]
        BSS_ACCTMANM_JSESSIONID_dict={BSS_ACCTMANM_JSESSIONID_key:BSS_ACCTMANM_JSESSIONID_value}
        # logging.warn(BSS_ACCTMANM_JSESSIONID_dict)
        # logging.warn("before",cookie_out)
        cookie_out.update(BSS_ACCTMANM_JSESSIONID_dict)
        # logging.warn("after",cookie_out)
        # logging.warn(type(cookie_out))
        data=requests.post(post_url,data=data,headers=post_headers,cookies=cookie_out,verify= False).content.decode("gbk")
        logging.warning(data)
    def parse(self, response):
        logging.debug("=====start parse========")
        pass
