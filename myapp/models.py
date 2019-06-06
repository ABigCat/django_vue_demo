# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, field ,tokenizer,token_filter,\
    analyzer, InnerObjectWrapper, Completion, Keyword, Text, Integer

from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"]) #大小写转换（搜索时忽略大小写影响）

my_pinyin_filter = token_filter('my_pinyin_filter', 'pinyin',
                                keep_separate_first_letter=False,
                                keep_full_pinyin=False,
                                keep_joined_full_pinyin=True,
                                limit_first_letter_length=16,
                                keep_original=True,
                                keep_none_chinese=False,
                                remove_duplicated_term=True,
                                lowercase=True)

my_pinyin_analyzer =analyzer('my_pinyin_analyzer',
                               tokenizer="ik_max_word",
                               filter=['lowercase', my_pinyin_filter])



class MovieType(DocType):
    # 为了实现搜索提示，添加一个completion字段
    # 由于使用ik_max_word，会出错，所以我们需要自己定义分析器，这样可以避免报错问题
    # 在item中定义生成建议的函数来处理字段 title和movieInfo，并附上各自的权重）https://www.jianshu.com/p/46eb88a4e489
    # suggest = Completion(analyzer=ik_analyzer)
    # 电影排序
    order = Keyword()
    # 电影名称
    title = Text(analyzer="ik_max_word", fields={'pinyin': Text(analyzer=my_pinyin_analyzer,
                                                                search_analyzer=my_pinyin_analyzer,
                                                                store=False,
                                                                term_vector="with_offsets",
                                                                boost=3)})
    # 评分
    star = Keyword()
    # 电影的描述信息，包括导演、主演、电影类型等等
    movie_info = Text(analyzer="ik_max_word")
    # # 电影中最经典或者说脍炙人口的一句话
    # quote = Text(analyzer="ik_max_word")
    # 图片链接
    image_url = Keyword()
    # 电影详情链接
    movie_url = Keyword()
    # 电影来源(例：douban,maoyan)
    movie_origin = Keyword()

    class Meta:
        # 数据库名称和表名称
        index = "movie"
        doc_type = "top"

    class Index:
        # 数据库名称和表名称
        name = "movie"
        doc_type = "top"

if __name__ == '__main__':
    MovieType.init()