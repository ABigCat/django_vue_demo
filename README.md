# Scrapy + Elasticsearch5.5.3 + Django2.2 + Vue 搜索引擎

## 一、Requirements

#### 1、后端

(1) 环境
- python：3.7.1
- pycharm：最好是2018.1.1后面的版本，pip版本从9.0.x升到10.0.x时，Api有些变化，而pycharm2018.1.1之前的版本都是按照旧版pip执行安装，安装东西时可能报错。

(2)安装后端所需环境
可能会出一点问题，建议先把scrapy相关的包先安装好，有些包需要自己手动安装，[参考文章](https://baijiahao.baidu.com/s?id=1597465401467369572&wfr=spider&for=pc)

```
    pip install -r requirements.txt
```

(3)运行
前端构建完成后，后端在teminal中执行（虚拟环境要处于打开的状态）

```
    python manage.py runserver 127.0.0.1:8000
```

#### 2、ES

- [ES5.5.3下载地址](https://www.elastic.co/cn/downloads/past-releases/elasticsearch-5-5-3)

- [ik分词器5.5.3下载地址](https://github.com/medcl/elasticsearch-analysis-ik/releases/tag/v5.5.3)
 （ES和ik版本必须一致，否则会报错）
 
- ElasticSearch Head 插件(如果可以科学上网，直接在应用商店添加；不能的话可以把插件拖到扩展程序中，这里有好多个[Chrome插件下载的网址](https://zhuanlan.zhihu.com/p/35802469)，下载插件后自己百度安装教程，一般拖到Google的扩展程序里就可以了。

#### 3、前端 

(1)  [node.js下载](https://nodejs.org/zh-cn/download/)

(2)  在terminal中执行以下命令，安装前端所需依赖:
```
    // 打开前端目录
    cd appfront
    
    // 安装前端所需依赖
    npm install
```
(3) 运行以及打包

```
    // 运行 localhost:8080
    npm run dev
    
    // 打包，后端django的Template的目录就是打包后生成的目录，appfront/dist
    npm run build
```
## 二、项目创建相关:

[spider项目创建以及运行](https://blog.csdn.net/l2535460824/article/details/89883119)

[django项目创建以及运行](https://blog.csdn.net/l2535460824/article/details/89883261)

[vue项目创建以及运行](https://blog.csdn.net/l2535460824/article/details/89883306)

[整合django+Vue](https://blog.csdn.net/l2535460824/article/details/89883345)

## 三、Problem
#### 2019/5/3

**错误**： elasticsearch5.5.3启动失败，出现如下提示：

```
Java HotSpot(TM) 64-Bit Server VM warning: INFO: os::commit_memory(0x0000000085330000, 2060255232, 0) failed; 
error='Cannot allocate memory' (errno=12)
```
**解决**：由于elasticsearch5.0默认分配jvm空间大小为2g，修改jvm空间分配

&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160; &#160;&#160; 打开ElasticSearch/config/jvm.options
```
        -Xms2g
        -Xmx2g
```

&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160; &#160;&#160; 修改为
```
        -Xms512m
        -Xmx512m
```

#### 2019/5/4：

##### 1. redis部分

&#160;&#160;&#160;&#160;&#160;&#160;&#160;问题：redis_cli.zincrby("hot_search", key_words)在es6.7.0下报错缺少value 
  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;解决：加入增量，redis_cli.zincrby("hot_search",1,key_words)

##### 2. 在python3中，关于redis读取数据带有‘b’的问题

&#160;&#160;&#160;&#160;&#160;&#160;&#160;问题：存进去的是字符串类型的数据，取出来却是字节类型的，这是由于python3的与redis交互的驱动的问题，Python2取出来的就是字符串类型的。

&#160;&#160;&#160;&#160;&#160;&#160;&#160;解决：加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。

#### 2019/5/5:

##### ES版本问题！！！ 

&#160;&#160;&#160;&#160;&#160;&#160;&#160;问题：
```
  elasticsearch.exceptions.RequestError: 
  TransportError(400, 'invalid_type_name_exception', 
  "Document mapping type name can't start with '_', found: [_suggest]")
```

&#160;&#160;&#160;&#160;&#160;&#160;&#160;解决：搜索提示部分出错，将本地ES降级到5.5.3，同时要下载同版本的ik分词器
## 四、说明
#### 本搜索引擎主要功能如下：
##### 1.基本搜索
##### 2.热门搜索
##### 3.搜索提示
##### 4.拼音搜索
- 拼音搜索这里使用ik+pinyin两个插件自定义分词器。
- pinyin分词器github地址 （https://github.com/medcl/elasticsearch-analysis-pinyin）
- Elasticsearch DSL([5.4.0文档地址](https://elasticsearch-dsl.readthedocs.io/en/5.4.0/index.html)),
因为最初创建索引的模型使用elasticsearch-dsl中的Doctype中创建的，想把网上创建pinyin分词器的写法转换成用elasticsearch-dsl实现，尝试了一些，最后自定义的分词器如下，

```
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
```

然后给需要的字段添加fileds，

```
     title = Text(analyzer="ik_max_word", fields={'pinyin': Text(analyzer=my_pinyin_analyzer,
                                                                    search_analyzer=my_pinyin_analyzer,
                                                                    store=False,
                                                                    term_vector="with_offsets",
                                                                    boost=3)})
```



