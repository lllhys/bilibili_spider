# -*- coding: utf-8 -*-
import requests
import scrapy
import scrapy_redis
from scrapy_redis.spiders import RedisSpider
import logging
from scrapy.exceptions import CloseSpider

from bilibili import settings
from bilibili.items import UploaderItem
from bilibili.items import FollowItem
from bilibili.items import FollowListItem

import json
import time
import bilibili.settings

logger = logging.getLogger(__name__)


class BilibiliSpiderSpider(RedisSpider):
    name = 'bilibili_spider'
    # allowed_domains = ['bilibili.com']
    # 启动爬虫的命令
    redis_key = settings.REDIS_START_URLS_KEY

    followings_url = 'https://api.bilibili.com/x/relation/followings?pn=%s&ps=50&order=desc&vmid=%s'
    fans_follows_url = 'https://api.bilibili.com/x/relation/stat?vmid='
    fans_follows_headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Referer': 'https://space.bilibili.com'
    }


    def parse(self, response):
        try:
            # 若settings中HTTPERROR_ALLOW_ALL = True，则需检测状态吗
            if response.status not in [200,301, 302, 303, 307]:
                raise CloseSpider("网址:%s 状态码异常:%s" % (response.url, response.status))
        except CloseSpider as error:
            logger.error(error)
        else:
            try:
                # 解析json数据
                json_data = json.loads(response.text)
            except Exception as error:
                # 若解析错误，记录url
                json_data = {"code": 403}
                logger.error((response.url, error))
                with open("./error_json.txt", "a") as fb:
                    fb.write(response.url)
                    fb.write("\n")
            logger.warning('当前爬取id'+response.url.split('=')[-1])
            now_id = int(response.url.split('=')[-1])
            followings = list()
            if json_data["code"] == 0:
                # 解析json数据，若为"--"则计为0
                data = json_data["data"]
                list_data = data.get('list')
                for up in list_data:
                    # 每个up主返回
                    item = UploaderItem()
                    item['id'] = up.get('mid')
                    item['name'] = up.get('uname')
                    item['face_url'] = up.get('face')
                    item['auth_description'] = up.get('sign')
                    # get fans and follows
                    url = self.fans_follows_url + str(item['id'])
                    res = requests.get(url, headers=self.fans_follows_headers)
                    item['follower_number'] = json.loads(res.text).get('data').get('follower')
                    item['following_number'] = json.loads(res.text).get('data').get('following')
                    # 添加一个follow Item
                    follow_item = FollowItem()
                    follow_item['following_id'] = now_id
                    follow_item['follower_id'] = item['id']
                    followings.append(follow_item)
                    yield item

                # # 添加后续页面url
                # pages = data.get('total') // 50
                # request_pages = pages if pages<=5 else 5
                # for page in range(2,request_pages+1):
                #     url = self.followings_url%(page,)
                #     scrapy.Request()

                # 当前up主结束，返回一个follow list item
                follow_list_item = FollowListItem()
                follow_list_item['follow_list'] = followings
                yield follow_list_item
                # 添加新的url
                for  up in list_data:
                    # 添加up页面去爬取
                    url = self.followings_url %(1,up.get('mid'))
                    # 添加到优先队列
                    yield scrapy.Request(url)


            logger.info("爬取完成:%s" % response.url)
        # 因logging等级设为了WARNING，则在log中增加一条完成记录
        logger.warning("完成:[%s]" % response.url)



