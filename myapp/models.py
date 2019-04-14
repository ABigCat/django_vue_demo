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

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class MovieType(DocType):
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
        index = "douBanMovie"
        doc_type = "top"

    class Index:
        # 数据库名称和表名称
        name = "douBanMovie"
        doc_type = "top"

if __name__ == '__main__':
    MovieType.init()