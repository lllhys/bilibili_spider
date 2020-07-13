# -*- coding: utf-8 -*-


'''
   本地配置
'''
# 指定bilibili登录用户名密码
BILIBILI_USERNAME = '****'
BILIBILI_PASSWORD = '****'

# 头像存储路径
IMAGES_STORE = '../face_image/'

# 指定连接到redis时使用的端口和地址
# 与代理ip公用设置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_PROXY_DB = 0

# Redis 存储键
REDIS_START_URLS_KEY = 'bilibili_spider:start_urls'
REDIS_COOKIES_KEY = 'bilibili_spider:cookies'
REDIS_PROXY_KEY = 'bilibili_spider:use_proxy'

# Mysql配置
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'bilibili'
MYSQL_USER = 'bilibili'
MYSQL_PASSWD = 'bilibili'




'''
    scrapy 配置
'''

SPIDER_MODULES = ['bilibili.spiders']
NEWSPIDER_MODULE = 'bilibili.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'bilibili (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 爬虫并发线程数，根据机器性能修改
# CONCURRENT_REQUESTS = 1024

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
# 每个domain并发量，设置为超大值，代表不限制
# CONCURRENT_REQUESTS_PER_DOMAIN = 100000000
# 单个ip并发量，设置为0，代表不限制
CONCURRENT_REQUESTS_PER_IP = 3

# Disable cookies (enabled by default)
# 禁用cookies
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# 不使用Telnet远程调试
TELNETCONSOLE_ENABLED = False


# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 设置默认user agent
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

DOWNLOADER_MIDDLEWARES = {
    # 重试
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 530,
    # 代理ip
    'bilibili.middlewares.BilibiliDownloaderMiddleware': 540,
    # 随机user agent
    'bilibili.middlewares.UserAgentmiddleware': 544,
}

ITEM_PIPELINES = {
    'bilibili.pipelines.BilibiliPipeline': 300,
    'bilibili.pipelines.BilibiliFacePiplines':301
    # 若希望保存item在redis中则打开RedisPipeline
    # 'scrapy_redis.pipelines.RedisPipeline': 310,
}

# 允许所有状态码通过
# HTTPERROR_ALLOW_ALL = True

# 重试次数
RETRY_ENABLED = True
RETRY_TIMES = 10

# 下载超时
DOWNLOAD_TIMEOUT = 10

# log日志设置
# LOG_FILE = 'mySpider.log'
LOG_LEVEL = 'DEBUG'
# LOG_LEVEL = 'WARNING'



#########################################################################
# Scrapy-Rdis配置项
# 启用Redis调度存储请求队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 确保所有的爬虫通过Redis去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 默认请求序列化使用的是pickle 但是我们可以更改为其他类似的。PS：这玩意儿2.X的可以用。3.X的不能用
# SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

# 不清除Redis队列、这样可以暂停/恢复 爬取
# SCHEDULER_PERSIST = True

# 使用优先级调度请求队列 （默认使用）
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
# REDIS_START_URLS_AS_ZSET = True
# 可选用的其它队列
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# 最大空闲时间防止分布式爬虫因为等待而关闭
# 这只有当上面设置的队列类是SpiderQueue或SpiderStack时才有效
# 并且当您的蜘蛛首次启动时，也可能会阻止同一时间启动（由于队列为空）
# SCHEDULER_IDLE_BEFORE_CLOSE = 10



# 自定义的redis参数（连接超时之类的）
# REDIS_PARAMS  = {}


# 如果为True，则使用redis的'spop'进行操作。
# 如果需要避免起始网址列表出现重复，这个选项非常有用。开启此选项urls必须通过sadd添加，否则会出现类型错误。
# REDIS_START_URLS_AS_SET = False

