# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

__browser_url = r'Z:\Users\wumingxing\AppData\Roaming\360se6\Application\360se.exe'  ##360浏览器的地址
# driver_path = "Z:/tools/chromedriver.exe"
# driver_path="Z:/Users/wumingxing/Downloads/chromedriver.exe"
driver_path = "Z:/tools/IEDriverServer.exe"
option=webdriver.IeOptions()
# option=webdriver.ChromeOptions()

option.binary_location=__browser_url
# driver=webdriver.Chrome(driver_path,options=option)
driver=webdriver.Ie(driver_path,options=option)
driver.get('https://cbss.10010.com')
time.sleep(10)
driver.quit()
