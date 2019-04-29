# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import redis
import scrapy
from myapp.models import MovieType
from elasticsearch_dsl.connections import connections

# 连接elasticsearch(搜索引擎)，使用操作搜索引擎的类下面的_doc_type.using连接
es = connections.create_connection(MovieType._doc_type.using)
redis_cli = redis.StrictRedis()
# """
#      此函数主要用于,连接elasticsearch(搜索引擎)，使用ik_max_word分词器，将传入的字符串进行分词，返回分词后的结果
#      此函数需要两个参数：
#      第一个参数：要调用elasticsearch(搜索引擎)分词的索引index，一般是（索引操作类._doc_type.index）
#      第二个参数：是一个元组，元祖的元素也是元组，元素元祖里有两个值一个是要分词的字符串，第二个是分词的权重，多个分词传多个元祖如下
#      书写格式：
#      gen_suggest(lagouType._doc_type.index, ((‘字符串‘, 10),(‘字符串‘, 8)))
# """


def gen_suggests(index,info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 字符串不为空时，调用elasticsearch的analyze接口分析字符串（分词、大小写转换）
            words =  es.indices.analyze(index=index, body={'text': text, 'analyzer':"ik_max_word",'filter':["lowercase"]})
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    return suggests

class MovieSpiderItem(scrapy.Item):
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
        movietype.suggest = gen_suggests(MovieType._doc_type.index, ((movietype.title, 10),(movietype.quote, 7)))
        movietype.save()
        return