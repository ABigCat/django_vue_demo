# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from . import settings


class MovieSpiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 存储到es
        # item.save_to_es()
        print(item)
        # 存储到数据库
        try:
            self.cursor.execute(
                """insert into top(title,star,movie_info,image_url,movie_order,movie_url,movie_origin)
                  values(%s,%s,%s,%s,%s,%s,%s)""",
                (item['title'],
                 item['star'],
                 item['movie_info'],
                 item['image_url'],
                 item['order'],
                 item['movie_url'],
                 item['movie_origin']))
            self.connect.commit()
        except Exception as err:
            print("错误信息为：" + str(err))
        return item
