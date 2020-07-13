# bilibili_spider
A bilibili distribute spider project about uploader's following relationship

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![license](https://img.shields.io/github/license/:user/:repo.svg)](https://github.com/llllhy/bilibili_spider/blob/master/LICENSE)

# Features
 - Use Scrapy-redis to build up distribute feature.
 - Use [jhao104/proxy_pool]("https://github.com/jhao104/proxy_pool") to build up proxy IP pool.
 - Save data to MySQL.

# Configuration
Before you run this project. You need to config the settings.py file.
In this file, you need to put you local information into some setting variables.  
```python
# 指定bilibili登录用户名密码
BILIBILI_USERNAME = '****'
BILIBILI_PASSWORD = '****'

# 头像存储路径
IMAGES_STORE = '../face_image/'

# 指定连接到redis时使用的端口和地址
# 与代理ip公用设置
REDIS_HOST = 'Host ip'
REDIS_PORT = 6379
REDIS_PASSWORD = 'if no password put None'
REDIS_PROXY_DB = 'db'

# Redis 存储键 
REDIS_START_URLS_KEY = 'bilibili_spider:start_urls'
REDIS_COOKIES_KEY = 'bilibili_spider:cookies'
REDIS_PROXY_KEY = 'bilibili_spider:use_proxy'

# Mysql配置
MYSQL_HOST = 'host ip'
MYSQL_DBNAME = 'Your database name'
MYSQL_USER = 'Your database user'
MYSQL_PASSWD = 'Your database password'
```
# Usage
```shell script
python run.py
```

# Related efforts

We use d3.js to visualize the data which we crawling in this project.
[bilibili Visualization]("default")
# License

[MIT © Richard McRichface.](../LICENSE)