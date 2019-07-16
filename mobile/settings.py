# -*- coding: utf-8 -*-

# Scrapy settings for mobile project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'mobile'

SPIDER_MODULES = ['mobile.spiders']
NEWSPIDER_MODULE = 'mobile.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mobile (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 100
RANDOM_UA_TYPE="ie"
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'mobile.middlewares.MobileSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'mobile.middlewares.MobileDownloaderMiddleware': 299,
   # 'mobile.middlewares.ProxyServerMiddleware':1,
   'mobile.middlewares.RandomUserAgentMiddlware': 2,
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,

}
""" 启用阿布云限速设置 """
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.2  # 初始下载延迟
DOWNLOAD_DELAY = 0.2  # 每次请求间隔时间
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/toMobileDownloaderMiddlewarepics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
RANDOM_UA_TYPE = 'ie'
ITEM_PIPELINES = {
   'mobile.pipelines.MobilePipeline': 1,
   # 'mobile.pipelines.DiscountPipeline': 1,
}

# CRITICAL - 严重错误
# ERROR - 一般错误
# WARNING - 警告信息
# INFO - 一般信息
# DEBUG - 调试信息
# LOG_LEVEL = 'WARNING'
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# MYSQL_HOST = "localhost"
MYSQL_HOST = "WIN-EGP38V915TC"
MYSQL_DBNAME= "website"
MYSQL_USER= "root"
MYSQL_PASSWD= "root12#$"

#日志文件路径
# LOG_FILE = "Z:\\Users\\wumingxing\\Desktop\\test.log"
# LOG_FILE = "C:\\test.log"
# LOG_LEVEL = "INFO"