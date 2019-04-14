# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from myapp.models import MovieType

class MovieSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Item是保存爬取到的数据的容器；其使用方法和Python字典类似，
    # 并且提供了额外保护机制来避免拼写错误导致的未定义字段错误。
    title = scrapy.Field()  # 电影名字
    movieInfo = scrapy.Field()  # 电影的描述信息，包括导演、主演、电影类型等等
    star = scrapy.Field()  # 电影评分
    quote = scrapy.Field()  # 电影中最经典或者说脍炙人口的一句话
    movie_url = scrapy.Field()  # 电影的url
    image_url = scrapy.Field()  # 图片的url
    pass

    def save_to_es(self):
        movietype = MovieType()
        movietype.title = self["title"]
        movietype.movieInfo = self["movieInfo"]
        movietype.star = self["star"]
        movietype.quote = self["quote"]
        movietype.movie_url = self["movie_url"]
        movietype.image_url = self["image_url"]
        movietype.save()
        return
