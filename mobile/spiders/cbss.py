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
    driver_path="Z:\BaiduNetdiskDownload\IEDriverServer.exe"
    captha_image_url="https://hq.cbss.10010.com/image?mode=validate&width=60&height=20"
    userName=""
    passWd=""

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        driver = webdriver.Ie(self.driver_path)
        res=driver.get(self.login_url)
        time.sleep(2)
        # driver.maximize_window()
        driver.find_element_by_id("STAFF_ID").send_keys(self.userName)
        driver.find_element_by_id("LOGIN_PASSWORD").send_keys(self.passWd)
        Select(driver.find_element_by_name("LOGIN_PROVINCE_CODE")).select_by_value("17")
        # captcha_url = driver.find_element_by_xpath("//div[@id='VerifyPart2']/img/@src")
        # logging.debug((captcha_url))
        captcha_image = requests.get(self.captha_image_url,verify=False)
        # 打开验证码图片
        img = Image.open(BytesIO(captcha_image.content))
        # 显示验证码
        img.show()
        # 输入识别出的验证码
        captcha_text = input(u'请输入验证码:')
        driver.find_element_by_id("VERIFY_CODE").send_keys(captcha_text)
        driver.find_element_by_xpath("//div[@class='submit clear']/input[1]").click()
        # all_options = select.find_elements_by_tag_name("option")
        logging.debug("------start------")
        WebDriverWait(driver, 1000).until(EC.url_to_be(self.initmy_url))
        logging.debug("恭喜您，您已登录成功了！")
        yield scrapy.Request(url=self.initmy_url, callback=self.parse)
    def parse(self, response):
        logging.debug("=====start parse========")
        ele=response.xpath("//div[@class='nav e_clearfix'])").extract()
        logging.debug(ele)
        pass
