# -*- coding: utf-8 -*-
import scrapy,logging,requests,time
from selenium.webdriver.support.select import Select
from scrapy.http import Request
from urllib import parse
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #期望的条件
from selenium.webdriver.common.by import By
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
    userName=""
    passWd=""

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        driver = webdriver.Ie(self.driver_path)
        driver.get(self.login_url)
        time.sleep(2)
        # driver.maximize_window()
        driver.find_element_by_id("STAFF_ID").send_keys(self.userName)
        driver.find_element_by_id("LOGIN_PASSWORD").send_keys(self.passWd)
        Select(driver.find_element_by_name("LOGIN_PROVINCE_CODE")).select_by_value("17")
        logging.debug("------start------")
        WebDriverWait(driver, 1000).until(EC.url_to_be(self.initmy_url))
        driver.implicitly_wait(3)
        logging.debug("恭喜您，您已登录成功了！")
        # 如果没有使用此行代码，则无法找到页面frame中的任何页面元素
        driver.switch_to.frame("navframe")
        time.sleep(25)
        logging.debug("========first menu click response==========")
        logging.debug(driver.page_source)
        # 获取财务管理a标签
        fmQuery_1 = driver.find_element_by_xpath("//li/a[@id='FIRST_MENU_LINK_BIL6000']")
        # logging.debug("=====================fmQuery_1===============")
        # logging.debug(fmQuery_1)
        fmQuery_1.click()
        time.sleep(25)
        logging.debug("========second menu click response==========")
        logging.debug(driver.page_source)
        # 获取财管查询a标签
        fmQuery_2 = driver.find_element_by_xpath("//div[@class='nav2 e_clearfix']/ul/li[12]/a")
        time.sleep(3)
        logging.debug(fmQuery_2)
        fmQuery_2.click()
        # time.sleep(15)
        # logging.debug("========third click response==========")
        # logging.debug(driver.page_source)




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
        # html = etree.HTML(response.text)
        # ele=response.xpath("//div[@class='nav e_clearfix'])").extract()
        # logging.debug(response.text)
        pass
