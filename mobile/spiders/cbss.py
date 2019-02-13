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
from pyquery import PyQuery as pq
import time,json
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
    # initmy_url = "https://sd.cbss.10010.com/abcde"
    # driver_path="Z:\BaiduNetdiskDownload\IEDriverServer.exe"
    driver_path = "Z:/tools/IEDriverServer.exe"
    captha_image_url="https://hq.cbss.10010.com/image?mode=validate&width=60&height=20"
    captha_image_path="Z:\\Users\\wumingxing\\Desktop\\printscreen.png"
    captha_image = "Z:\\Users\\wumingxing\\Desktop\\captha.png"
    userName=""
    passWd=""
    js_exec="var but_click=document.getElementsByClassName('submit')[0].children[0].onclick"
    # js_exec="var but_click=document.querySelector('.button')"
    reqeust_url="https://sd.cbss.10010.com/acctmanm?service=page/amarchquery.queryuserbill.QueryUserBillCBss&listener=myInitialize&RIGHT_CODE=ASMUSERTABQRY&LOGIN_RANDOM_CODE=15500242660371590672351&LOGIN_CHECK_CODE=201902131747274690&LOGIN_PROVINCE_CODE=17&IPASS_LOGIN=null&gray_staff_id=sdsc-xingyy7&gray_depart_id=17b5q7m&gray_province_code=17&gray_eparchy_code=0531&staffId=sdsc-xingyy7&departId=17b5q7m&subSysCode=CBS&eparchyCode=0531"
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
        WebDriverWait(driver, 30).until(EC.url_to_be(self.initmy_url))
        logging.debug("恭喜您，您已登录成功了！")
        # 如果没有使用此行代码，则无法找到页面frame中的任何页面元素
        driver.switch_to.frame("navframe")
        time.sleep(10)
        # logging.warning("=========first==========")
        # logging.warning(driver.page_source)
        js_query_acct="var query_acct=document.getElementById('SECOND_MENU_LINK_BIL6500').onclick()"
        # driver.execute_script(js_query_acct)
        time.sleep(3)
        # logging.warning("=========second==========")
        # logging.warning(driver.page_source)
        js_query_bill = "var query_acct=document.getElementById('BIL651P').onclick()"
        driver.execute_script(js_query_acct)
        logging.warning("=========third==========")
        # CSM1001=driver.find_element_by_id("CSM1001")
        CSM1001_js="document.getElementById('CSM1001').getAttribute('onclick')"
        CSM1001=driver.execute_script(CSM1001_js)
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
        res=s.get(self.reqeust_url,headers=headers,cookies=cookie_out,verify= False)
        time.sleep(5)
        logging.warning(res.content.decode('gbk'))
        # res.content
    def parse(self, response):
        logging.debug("=====start parse========")
        pass
