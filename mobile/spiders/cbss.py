# -*- coding: utf-8 -*-
import scrapy,logging
from scrapy.http import Request
from urllib import parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC #期望的条件
from selenium.webdriver.common.by import By
import time,json
import pickle
from scrapy.http.cookies import CookieJar


class CbssSpider(scrapy.Spider):
    name = 'cbss'
    allowed_domains = ['cbss.10010.coms']
    start_urls = ['https://cbss.10010.com/essframe']
    login_url = "https://cbss.10010.com/essframe"

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        driver = webdriver.Ie()
        driver.get(self.login_url)
        time.sleep(10)
        logging.debug(response.css(".li.userInfo"))
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.li.userInfo')))
        logging.debug("恭喜您，您已登录成功了！")
        logging.debug("------------")
    def parse(self, response):
        pass
