import json
from datetime import datetime

import redis
import pymysql
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from elasticsearch import Elasticsearch

from myapp.models import MovieType
from movie_spider.movie_spider import settings
client = Elasticsearch(hosts=["127.0.0.1"])

# problem：存进去的是字符串类型的数据，取出来却是字节类型的，这是由于python3的与redis交互的驱动的问题，Python2取出来的就是字符串类型的。
# answer：加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
redis_cli = redis.StrictRedis(decode_responses=True)

# Create your views here.
class IndexView(View):
    #首页
    def get(self, request):
        # 从request中获取所需参数
        # (1)获取当前页码
        currentPage = request.GET.get("currentPage", "1")
        try:
            currentPage = int(currentPage)
        except:
            currentPage = 1

        # (2)获取每页条数
        page_size = request.GET.get("page_size", "10")
        try:
            page_size = int(page_size)
        except:
            page_size = 10

        # (3)获取当前选择搜索的范围
        # data_source = request.GET.get("dataSource", "豆瓣top250")

        # redis 获取热门搜索/从redis查看该类数据总量
        hot_search = redis_cli.zrevrangebyscore("hot_search", "+inf", "-inf", start=0, num=5,withscores=True)
        douBanTop_count = redis_cli.get("douBanTop_count")

        # 获取全部数据
        datas = client.search(
            index="doubanmovie",
            body={
                "query": {
                    "match_all": {}
                },
                "from": (currentPage - 1) * page_size,
                "size": page_size
            }
        )
        # 数据总数
        total_nums = datas["hits"]["total"]
        # 总页数
        if (total_nums % page_size) > 0:
            page_nums = int(total_nums / page_size) + 1
        else:
            page_nums = int(total_nums / page_size)

        response_datas = []
        for item in datas["hits"]["hits"]:
            response_datas.append(item["_source"])
        # 返回前台数据
        return JsonResponse({"response_datas": response_datas,
                             "hot_search": hot_search,
                             "total_nums": total_nums,
                             "page_nums": page_nums
                             }, safe=False)
        # 关于JsonResponse https://www.cnblogs.com/guoyunlong666/p/9099397.html
        # 这个类是HttpResponse的子类，它主要和父类的区别在于：
        # 1.它的默认Content - Type
        # 被设置为： application / json
        # 2.第一个参数，data应该是一个字典类型，当 safe这个参数被设置为：False, 那data可以填入任何能被转换为JSON格式的对象，比如list, tuple, set。 默认的safe
        # 参数是True.如果你传入的data数据类型不是字典类型，那么它就会抛出TypeError的异常。

# Create your views here.
class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        print(key_words)
        re_datas = []
        if key_words:
            s = MovieType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 2
                },
                "size": 5
            })
            suggestions = s.execute_suggest()
            print(suggestions.my_suggest[0].options)
            for item in suggestions.my_suggest[0].options:
                source = item._source
                title = source["title"].split("/", 1)[0]
                re_datas.append({"value": title})
        return JsonResponse({"res_data": re_datas}, safe=False)



class SearchView(View):
    def get(self, request):
        # 从request中获取所需参数
        # (1)获取搜索关键字
        key_words = request.GET.get("s", "")
        # (2)获取当前页码
        currentPage = request.GET.get("currentPage", "1")
        try:
            currentPage = int(currentPage)
        except:
            currentPage = 1

        # (3)获取每页条数
        page_size = request.GET.get("page_size", "10")
        try:
            page_size = int(page_size)
        except:
            page_size = 10

        # (4)获取当前选择搜索的范围
        # data_source = request.GET.get("dataSource", "豆瓣top250")

        # redis部分
        # (1)添加搜索关键字(如果在键为name的zset中已经存在元素value，则将该元素的score增加amount；否则向该集合中添加该元素，其score的值为amount)
        # (2)重新获取热门搜索
        if key_words:
            redis_cli.zincrby("hot_search", 1, key_words)
        hot_search = redis_cli.zrevrangebyscore("hot_search", "+inf", "-inf", start=0, num=5, withscores=True)
        # (3)从redis查看该类数据总量
        douBanTop_count = redis_cli.get("douBanTop_count")


        # 开始查找
        start_time = datetime.now()
        # 根据关键字查找
        response = client.search(
            index="doubanmovie",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["title", "quote", "title.pinyin", "movieInfo"]
                    }
                },
                "from": (currentPage - 1) * page_size,
                "size": page_size,
                # 对关键字进行高光标红处理
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "title": {},
                        "quote": {}
                    }
                }
            }
        )
        # 结束时间
        end_time = datetime.now()
        # 耗时
        last_seconds = (end_time - start_time).total_seconds()
        # 数据总数
        total_nums = response["hits"]["total"]
        # 总页数
        if (total_nums % page_size) > 0:
            page_nums = int(total_nums / page_size) + 1
        else:
            page_nums = int(total_nums / page_size)

        hit_list = []
        for item in response["hits"]["hits"]:
            hit_list.append(item["_source"])
        print(hit_list)

        # for hit in response["hits"]["hits"]:
        #     hit_dict = {}
        #     if "title" in hit["highlight"]:
        #         hit_dict["title"] = "".join(hit["highlight"]["title"])
        #     else:
        #         hit_dict["title"] = hit["_source"]["title"]
        #     if "quote" in hit["highlight"]:
        #         hit_dict["quote"] = "".join(hit["highlight"]["quote"])[:500]
        #     else:
        #         hit_dict["quote"] = hit["_source"]["quote"][:500]
        #
        #     hit_dict["url"] = hit["_source"]["url"]
        #     hit_dict["score"] = hit["_score"]
        #
        #     hit_list.append(hit_dict)
        return JsonResponse({"all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,
                                                "hot_search": hot_search}, safe=False)


class SearchFromDBView(View):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def get(self, request):
        movie_origin = request.GET.get("movie_origin", "1")
        # 查询数据
        sql = """SELECT * FROM top WHERE movie_origin=%s """
        topMovies = []
        try:
            self.cursor.execute(sql, movie_origin)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                movie = {
                    "title": row[1],
                    "star": row[2],
                    "movie_info": row[3],
                    "movie_url": row[4],
                    "image_url": row[5],
                    "movie_origin": row[6],
                    "movie_order": row[7]
                }
                topMovies.append(movie)
        except Exception as err:
            print("错误信息为：" + str(err))
        return JsonResponse({ "result": topMovies })
