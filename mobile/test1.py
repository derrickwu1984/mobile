from selenium import  webdriver
from PIL import Image
from selenium.webdriver.support.select import Select
import  time,pytesseract,logging
import cv2 as cv

def snap_shot():
    userName="bjsc-wangj1"
    passWd="BySh@2019"
    province_id = "11"
    driver_path = "Z:/tools/IEDriverServer.exe"
    # driver_path = "Z:/tools/chromedriver.exe"
    driver = webdriver.Ie(driver_path)
    # driver = webdriver.Chrome(driver_path)
    driver.get("https://cbss.10010.com/essframe")
    driver.maximize_window()
    time.sleep(2)
    # driver.find_element_by_id("STAFF_ID").send_keys(userName)
    # driver.find_element_by_id("LOGIN_PASSWORD").send_keys(passWd)
    # Select(driver.find_element_by_name("LOGIN_PROVINCE_CODE")).select_by_value(province_id)
    # time.sleep(4)

    driver.save_screenshot("D:/bd.png")
    element = driver.find_element_by_id("captureImage")
    left = element.location['x']
    top = element.location['y']
    right = element.location['x']+element.size['width']
    bottom = element.location['y']+element.size['height']
    img = Image.open('D:/bd.png')
    img = img.crop((left,top,right,bottom))
    img.save('D:/2.png')
    # 0:读入灰度图 1：读入彩色图
    img = cv.imread('D:/2.png')
    # ret1,th1 = guassian_blur(img,5,5)
    # ret2, th2 = bilatrial_blur(img)
    # ret3,th3 = median_blur(img)
    # cv.imwrite('D:/temp1.png',th1)
    # cv.imwrite('D:/temp2.png', th2)
    # cv.imwrite('D:/temp3.png', th3)
    # img1 = Image.open('D:/temp1.png')
    # img2 = Image.open('D:/temp2.png')
    # img3 = Image.open('D:/temp3.png')
    # print ("img1=".format(pytesseract.image_to_string(img1,lang='eng')))
    # print("img2=".format(pytesseract.image_to_string(img2, lang='eng')))
    # print("img3=".format(pytesseract.image_to_string(img3, lang='eng')))

    result = recognize_text(img)

    # print ("图片文字={0}".format(result))
    # driver.close()

def recognize_text(src):
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 6))#去除线
    binl = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 1))
    open_out = cv.morphologyEx(binl, cv.MORPH_OPEN, kernel)
    cv.bitwise_not(open_out, open_out)  # 背景变为白色
    cv.imshow("转换", open_out)
    cv.waitKey(0)
    cv.destroyAllWindows()
    # 从np.array 转换成<class 'PIL.Image.Image'>，pytesseract需要接受此类型
    textImage = Image.fromarray(open_out)
    text = pytesseract.image_to_string(textImage)
    print ("识别结果={0}".format(text))
    return text

def guassian_blur(img,a,b):
    #(a,b)为高斯核的大小，0为标准差，一般情况a,b=5
    blur =cv.GaussianBlur(img,(a,b),0)
    #阈值一定要设置为0
    ret,th = otsu_s(blur)
    return ret,th
# 均值滤波器
def  hamogeneous_blur(img):
    blur = cv.blur(img,(5,5))
    ret,th = otsu_s(blur)
    return ret,th
# 中值滤波器
def median_blur(img):
    blur = cv.medianBlur(img,5)
    ret,th = otsu_s(blur)
    return ret,th
# 双边滤波器
def bilatrial_blur(img):
    blur = cv.bilateralFilter(img,9,75,75)
    ret,th = otsu_s(blur)
    return ret,th
def otsu_s(img):
    ret,th = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    return ret, th
snap_shot()