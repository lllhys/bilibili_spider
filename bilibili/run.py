import json
import os
import time
from http.cookiejar import LWPCookieJar, Cookie
import random

from redis import StrictRedis
from selenium import webdriver  # 导入库
from bilibili import settings

def bilibili_login(browser):
    # 如果redis有cookie 就加cookie
    browser.get('https:bilibili.com')
    while redis_db.llen(settings.REDIS_COOKIES_KEY) is not 0:
        # 获取cookie
        cookie_ori = eval(redis_db.lpop(settings.REDIS_COOKIES_KEY).decode())
        cookie = {'domain': cookie_ori['domain'], 'name': cookie_ori['name'], 'value': cookie_ori['value']}
        # print(cookie)
        browser.add_cookie(cookie)
    url = 'https:account.bilibili.com/account/home'
    browser.get(url)  # 打开浏览器预设网址
    # print(browser.page_source)  # 打印网页源代码
    time.sleep(2)
    if browser.current_url != 'https://account.bilibili.com/account/home':
        # 手动登录
        time.sleep(1)
        browser.find_element_by_id('login-username').send_keys(settings.BILIBILI_USERNAME)
        time.sleep(1)
        browser.find_element_by_id('login-passwd').send_keys(settings.BILIBILI_PASSWORD)
        time.sleep(1)
        browser.find_element_by_css_selector('.btn-login').click()
        # browser.close()  # 关闭浏览器
        time.sleep(10)
        # TODO 增加自动化完成选字验证码
    # 清空redis中的cookies
    redis_db.ltrim(settings.REDIS_COOKIES_KEY, 1, 0)
    # 获取登录的cookies
    cookies = browser.get_cookies()
    for cookie in cookies:
        # push
        redis_db.lpush(settings.REDIS_COOKIES_KEY, cookie)
    return browser

def random_get_follower(browser):
    # 跳转到关注页
    browser.get('https://www.bilibili.com/')
    time.sleep(2)
    url = browser.find_element_by_css_selector('a.count-item').get_attribute('href')
    browser.get(url)
    # 获取关注list
    follower_list = browser.find_elements_by_css_selector('li.list-item')
    # 随机选一个
    follow = follower_list[random.randint(0, len(follower_list)-1)]
    # 获取id
    follower_id = follow.find_element_by_css_selector('a.cover').get_attribute('href').split('/')[-2]
    return follower_id

def run():
    # 发送命令，启动一个爬虫
    cmd = "scrapy crawl bilibili_spider"
    os.system(cmd)

if __name__ == '__main__':
    redis_db = StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=0,
    )
    # 检查redis是否有url，如果有直接运行scrapy,没有就登录
    # llen = redis_db.zcard(settings.REDIS_START_URLS_KEY)

    llen = redis_db.llen(settings.REDIS_START_URLS_KEY)
    if llen == 0:
        # login
        browser = webdriver.Chrome('../chromedriver.exe')  # 声明浏览器
        # 登录以下
        bilibili_login(browser)
        # 休息5秒
        time.sleep(5)
        # 随机获取一个id
        follower_id = random_get_follower(browser)
        print('将从id为 %s 的up主开始爬取'%follower_id)
        # url lpush 到redis
        url = 'https://api.bilibili.com/x/relation/followings?pn=%s&ps=50&order=desc&vmid=%s'%(1,follower_id)
        print(url)
        redis_db.lpush(settings.REDIS_START_URLS_KEY,url)
        # redis_db.zadd(settings.REDIS_START_URLS_KEY,100,url)

    # 运行spider
    run()