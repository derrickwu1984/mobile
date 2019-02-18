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
import json
import datetime
import pickle
import sys
from PIL import Image
from io import BytesIO
from scrapy.http.cookies import CookieJar

# set default logging configuration
logger = logging.getLogger()  # initialize logging class
logger.setLevel(logging.WARNING)  # default log level
format = logging.Formatter("%(asctime)s - %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)  # output to standard output
sh.setFormatter(format)
logger.addHandler(sh)
class CbssSpider(scrapy.Spider):
    name = 'cbss'
    allowed_domains = ['cbss.10010.com']
    start_urls = ['https://cbss.10010.com/essframe']
    login_url = "https://cbss.10010.com/essframe"
    # 登陆后的链接
    initmy_url = "https://sd.cbss.10010.com/essframe"
    # driver_path="D:/tools/IEDriverServer.exe"
    driver_path = "Z:/tools/IEDriverServer.exe"
    captha_image_url="https://hq.cbss.10010.com/image?mode=validate&width=60&height=20"
    captha_image_path="Z:\\Users\\wumingxing\\Desktop\\printscreen.png"
    captha_image = "Z:\\Users\\wumingxing\\Desktop\\captha.png"
    userName=""
    passWd=""
    js_exec="var but_click=document.getElementsByClassName('submit')[0].children[0].onclick"

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)
    def login(self, response):
        driver = webdriver.Ie(self.driver_path)
        driver.get(self.login_url)
        time.sleep(5)
        driver.find_element_by_id("STAFF_ID").send_keys(self.userName)
        driver.find_element_by_id("LOGIN_PASSWORD").send_keys(self.passWd)
        Select(driver.find_element_by_name("LOGIN_PROVINCE_CODE")).select_by_value("17")
        # captha_input=input(u"请输入验证码:")
        # VERIFY_CODE_ELE = driver.find_element_by_id("VERIFY_CODE")
        # VERIFY_CODE_ELE.send_keys(captha_input)
        WebDriverWait(driver, 1000).until(EC.url_to_be(self.initmy_url))
        logging.debug("恭喜您，您已登录成功了！")
        # 如果没有使用此行代码，则无法找到页面frame中的任何页面元素
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'navframe')))
        driver.switch_to.frame("navframe")
        # time.sleep(30)
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID,'SECOND_MENU_LINK_BIL6500')))
        logging.debug("找到 SECOND_MENU_LINK_BIL6500")
        # in order to find CSM1001
        js_query_acct="var query_acct=document.getElementById('SECOND_MENU_LINK_BIL6500').onclick()"
        driver.execute_script(js_query_acct)
        time.sleep(3)
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'CSM1001')))
        CSM1001 = driver.find_element_by_id("CSM1001").get_attribute("onclick")
        CSM1001_content=CSM1001.split('&')
        LOGIN_RANDOM_CODE =CSM1001_content[3]
        LOGIN_CHECK_CODE=CSM1001_content[4]
        reqeust_url = "https://sd.cbss.10010.com/acctmanm?service=page/amarchquery.queryuserbill.QueryUserBillCBss&listener=myInitialize&RIGHT_CODE=ASMUSERTABQRY&"+LOGIN_RANDOM_CODE+"&"+LOGIN_CHECK_CODE+"&LOGIN_PROVINCE_CODE=17&IPASS_LOGIN=null&gray_staff_id=sdsc-xingyy7&gray_depart_id=17b5q7m&gray_province_code=17&gray_eparchy_code=0531&staffId=sdsc-xingyy7&departId=17b5q7m&subSysCode=CBS&eparchyCode=0531"
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
        }
        yield scrapy.Request(reqeust_url,headers=headers,cookies=cookie_out,callback=self.parse_billPage,meta={'reqeust_url':reqeust_url})
        # data=requests.post(post_url,data=data,headers=post_headers,cookies=cookie_out,verify= False).content.decode("gbk")
    def parse_billPage(self,response):
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
        post_url="https://sd.cbss.10010.com/acctmanm;"+BSS_ACCTMANM_JSESSIONID
        headNo='1301171'
        for subNo in range(8800,8889):
            phoneNo=headNo+str(subNo).zfill(4)
            cond_NET_TYPE_CODE=''
            cond_PARENT_TYPE_CODE=''
            cond_ROUTE_EPARCHY_CODE='0531'
            data=self.prepare_data(query_month,"13011718888",cond_NET_TYPE_CODE,cond_PARENT_TYPE_CODE,cond_ROUTE_EPARCHY_CODE,Form0,service)
            BSS_ACCTMANM_JSESSIONID_array=BSS_ACCTMANM_JSESSIONID.split("=")
            BSS_ACCTMANM_JSESSIONID_key=BSS_ACCTMANM_JSESSIONID_array[0]
            BSS_ACCTMANM_JSESSIONID_value = BSS_ACCTMANM_JSESSIONID_array[1]
            BSS_ACCTMANM_JSESSIONID_dict={BSS_ACCTMANM_JSESSIONID_key:BSS_ACCTMANM_JSESSIONID_value}
            with open('cookies.txt', 'r') as f:
                cookie_billPage = json.load(f)
            cookie_billPage.update(BSS_ACCTMANM_JSESSIONID_dict)
            post_headers = {
                'referer':reqeust_url,
                'Host':'sd.cbss.10010.com',
            }
            time.sleep(3)
            yield scrapy.FormRequest(url=post_url, formdata=data, method="POST",cookies=cookie_billPage, callback=self.parse,meta={'phoneNo':"13011718888"})
    def prepare_data(self,query_month,phoneNo,cond_NET_TYPE_CODE,cond_PARENT_TYPE_CODE,cond_ROUTE_EPARCHY_CODE,Form0,service):
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
    def parse(self, response):
        response_str=response.body.decode("gbk")
        html = etree.HTML(response_str)
        phoneNo=response.meta['phoneNo']
        error_msg =""
        try:
            error_msg=html.xpath("//div[@class='tip']/ul/li/text()")[0].split("：")[0]
        except:
            # logging.warning("未发现错误提示")
            pass
        # finally:
        #     logging.warning ("It is not error page!")
        if (error_msg!="" and "错误提示"==error_msg):
            logging.warning(phoneNo+"手机号未查询到或已被注销！")
        else:
            logging.warning(phoneNo+"手机号码有效！")
            acctflag=html.xpath("//table/tr/td[2]//text()")[12].strip()
            paytype=html.xpath("//table/tr/td[2]//text()")[13].strip()
            debtfee=html.xpath("//table/tr/td[2]//text()")[14].strip()
            fixtype=html.xpath("//table/tr/td[2]//text()")[15].strip()
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
            logging.warning(html.xpath("//table/tr/td[8]//text()"))
            logging.warning(acctflag)
            logging.warning(paytype)
            logging.warning(debtfee)
            logging.warning(fixtype)
            logging.warning(fee)
            logging.warning(prodname)
            logging.warning(fee)
            logging.warning(openflag)
            logging.warning(custbrand)
            logging.warning(actualbal)
            logging.warning(totalfee)
            logging.warning(creditbal)
            logging.warning(custlocation)
            logging.warning(actualfee)
        return
