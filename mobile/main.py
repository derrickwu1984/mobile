from scrapy.cmdline import execute
import  logging,_thread

# def mutil_process(thread_name,rangeNo):
#     print("%s:%s" % (thread_name, rangeNo))
execute(["scrapy", "crawl", "cbss", "-a", "rangeNo=1860008", "-a", "startNo=0000", "-a", "endNo=10000"])

# try:
#     _thread.start_new_thread(mutil_process,("thread-1","1300017",))
    # _thread.start_new_thread(mutil_process,("thread-2","1310531",))
# except:
#     print ("error:unable to start thread")
# while 1:
#     pass