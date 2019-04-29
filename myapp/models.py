# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"]) #大小写转换（搜索时忽略大小写影响）

class MovieType(DocType):
    # 为了实现搜索提示，添加一个completion字段
    # 由于使用ik_max_word，会出错，所以我们需要自己定义分析器，这样可以避免报错问题
    # 在item中定义生成建议的函数来处理字段 title和movieInfo，并附上各自的权重）https://www.jianshu.com/p/46eb88a4e489
    suggest = Completion(analyzer=ik_analyzer)
    # 电影名称
    title = Text(analyzer="ik_max_word")
    # 评分
    star = Keyword()
    # 电影的描述信息，包括导演、主演、电影类型等等
    movieInfo = Text(analyzer="ik_max_word")
    # 电影中最经典或者说脍炙人口的一句话
    quote = Text(analyzer="ik_max_word")
    # 图片链接
    image_url = Keyword()
    # 电影详情链接
    movie_url = Keyword()

    class Meta:
        # 数据库名称和表名称
        index = "doubanmovie"
        doc_type = "top"

    class Index:
        # 数据库名称和表名称
        name = "doubanmovie"
        doc_type = "top"

if __name__ == '__main__':
    MovieType.init()