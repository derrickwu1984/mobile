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
    js_method="clickMenuItem(this);openmenu('/acctmanm?service=page/amarchquery.queryaccountbill.QueryAccountBill&listener=myInitialize&RIGHT_CODE=BIL651P&LOGIN_RANDOM_CODE=1548903104099624120380&LOGIN_CHECK_CODE=201901311746371775&LOGIN_PROVINCE_CODE=17&IPASS_LOGIN=null&gray_staff_id=sdsc-xingyy7&gray_depart_id=17b5q7m&gray_province_code=17&gray_eparchy_code=0531');"
    js_exec="var but_click=document.getElementsByClassName('submit')[0].children[0].onclick"
    # js_exec="var but_click=document.querySelector('.button')"
    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        driver = webdriver.Ie(self.driver_path)
        driver.get(self.login_url)
        time.sleep(2)
        builder=ActionChains(driver)
        # builder.send_keys(Keys.F12).perform()
        time.sleep(2)
        driver.refresh()
        time.sleep(5)
        driver.find_element_by_id("STAFF_ID").send_keys(self.userName)
        driver.find_element_by_id("LOGIN_PASSWORD").send_keys(self.passWd)
        Select(driver.find_element_by_name("LOGIN_PROVINCE_CODE")).select_by_value("17")
        time.sleep(2)
        # driver.save_screenshot(self.captha_image_path)
        # locate_image=driver.find_element_by_id("captureImage").location
        # size_image=driver.find_element_by_id("captureImage").size
        # left=locate_image['x']
        # top=locate_image['y']
        # right=locate_image['x']+size_image['width']
        # bottom = locate_image['y']+size_image['height']

        # rangle=(int (left),int(top),int(right),int(bottom))
        # i = Image.open(self.captha_image_path)
        # segment  = i.crop(rangle)
        # segment.save(self.captha_image)
        # i = Image.open(self.captha_image)
        # i.show()
        captha_input=input(u"请输入验证码:")
        VERIFY_CODE_ELE = driver.find_element_by_id("VERIFY_CODE")
        VERIFY_CODE_ELE.send_keys(captha_input)
        time.sleep(2)
        # above=driver.find_element_by_class_name("submit")
        above = "var submit_div=document.getElementsByClassName('submit')[0].children[0]"
        time.sleep(2)
        # driver.execute_script(self.js_exec)

        # driver.execute_script("checkIpassState()")

        # login_button = driver.find_elements_by_css_selector(".button.buttonOver")
        logging.debug("------start------")
        WebDriverWait(driver, 30).until(EC.url_to_be(self.initmy_url))
        logging.debug("恭喜您，您已登录成功了！")
        # 如果没有使用此行代码，则无法找到页面frame中的任何页面元素

        driver.switch_to.frame("navframe")
        logging.warning(driver.page_source)
        # time.sleep(25)
        # first_menu = driver.find_element_by_id("FIRST_MENU_LINK_BIL6000")
        # logging.warning("==========first_menu_assert===========")
        # assert first_menu.is_displayed()
        # first_menu.click()
        # logging.debug("==========after click first_menu response==============")
        # logging.debug(driver.page_source)
        # time.sleep(30)
        # second_menu=driver.find_element_by_id("SECOND_MENU_LINK_BIL6500")
        # logging.warning("==========second_menu===========")
        # logging.warning(second_menu)
        # for i in range(3):
        #     try:
        #         assert second_menu.is_displayed()
        #     except :
        #         logging.error("no Element displayed")
        #     else:
        #         second_menu.click()
        # logging.debug("==========after click second_menu response==============")
        # logging.debug(driver.page_source)
        # driver.execute_script(self.js_method)
        # logging.warning(driver.execute_script(self.js_method))
        # a_tag=driver.find_element_by_id("BIL651P")
        # logging.warning(a_tag)
        # a_tag.click()
        cookies_dict = {}
        cookies = driver.get_cookies()
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        with open('cookies.txt', 'w+') as f:
            json.dump(cookies_dict, f)
        with open('cookies.txt', 'r') as f:
            cookie_out = json.load(f)
            logging.debug(cookie_out)
        headers = {
            'referer': 'https://cbss.10010.com/essframe',
            'cookie': cookie_out
        }
        # yield scrapy.Request(url=self.initmy_url, callback=self.parse,headers=headers)
    def parse(self, response):
        logging.debug("=====start parse========")
        pass
