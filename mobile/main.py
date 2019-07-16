from scrapy.cmdline import execute
import  logging,sys,re

execute(["scrapy", "crawl", "cbss", "-a", "rangeNo=1860001" , "-a", "startNo=0000", "-a", "endNo=10000"])
# phoneNo= sys.argv[1]
# if (re.findall("1[345678][01256]\d{4}",phoneNo) and len(phoneNo)==7):
#     execute(["scrapy", "crawl", "cbss", "-a", "rangeNo="+phoneNo, "-a", "startNo=0000", "-a", "endNo=10000"])
# else:
#     logging.warning("请输入符合联通号段规则的7位电话号段！")
#