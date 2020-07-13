# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymysql
import logging
import os

import pymysql
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from bilibili.items import UploaderItem
from bilibili.items import FollowListItem
from bilibili import settings
import logging as logger
import time
from pymongo import MongoClient


class BilibiliPipeline(object):
    # def __init__(self):
    #     # 建立数据库连接
    #     client = MongoClient(settings["MONGO_HOST"], settings["MONGO_PORT"])
    #     # 连接目标数据库
    #     db = client["bilibili"]
    #     db.authenticate(settings["MONGO_USERNAME"], settings["MONGO_PASSWORD"])
    #     # 连接集合
    #     # 根据当前日期建立集合
    #     col_name = "b_video_stat_" + time.strftime("%Y%m%d")
    #     col = db[col_name]
    #
    #     self.col = col
    #
    # def process_item(self, item, spider):
    #     try:
    #         data = dict(item)
    #         self.col.insert_one(data)
    #     except Exception as error:
    #         # 记录保存错误的url
    #         logger.error(error)
    #         with open("./error_mongo.txt", "a") as fb:
    #             fb.write("aid:" + str(item["aid"]))
    #             fb.write("\n")
    #     return item

    # 保存到mysql
    def process_item(self, item, spider):
        # 连接数据库
        connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8mb4',
            use_unicode=True)

        # 通过cursor执行增删查改
        cursor = connect.cursor()
        try:
            if isinstance(item,UploaderItem):
                sql = '''insert into uploader(id, name, auth_description, following_number, follower_number)
                                    values (%d,'%s','%s',%d,%d)''' % (item["id"],
                                                                        item["name"],
                                                                        # item["face_url"],
                                                                        item["auth_description"],
                                                                        item["following_number"],
                                                                        item["follower_number"])
                cursor.execute(sql)
                # 提交sql语句
                connect.commit()
            elif isinstance(item,FollowListItem):
                for follow in item['follow_list']:
                    sql = '''insert into follow(following_id, follower_id) values(%d,%d)''' %(follow['following_id'],follow['follower_id'])
                    cursor.execute(sql)
                    # 提交sql语句
                    connect.commit()

        except Exception as error:
            # 出现错误时打印错误日志
            logging.error((error, item))

        connect.close()
        return item


class BilibiliFacePiplines(ImagesPipeline):

    # 重写方法
    def get_media_requests(self, item, info):
        if isinstance(item, UploaderItem):
            if os.path.exists(settings.IMAGES_STORE + str(item["id"]) + ".jpg"):
                logger.warning('文件存在，跳过')
                pass
            else:
                image_url = item["face_url"]
                yield scrapy.Request(image_url)
        pass
    # 保存图片时重命名
    def item_completed(self, results, item, info):
        if isinstance(item, UploaderItem):
            if os.path.exists(settings.IMAGES_STORE + str(item["id"]) + ".jpg"):
                logger.warning('文件存在，跳过')
                pass
            else:
                path = results[0][1]['path']
                # print(path)
                # 重命名
                try:
                    os.rename(settings.IMAGES_STORE+path, settings.IMAGES_STORE + str(item["id"]) + ".jpg")
                except Exception:
                    logger.error('文件重复')
        pass