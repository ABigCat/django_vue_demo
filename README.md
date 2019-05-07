[github地址](https://github.com/ABigCat/Django_Vue_Demo)
## 一、Requirements
#### 1、后端
(1) 环境
- python：3.7.1
- pycharm：最好是2018.1.1后面的版本，pip版本从9.0.x升到10.0.x时，Api有些变化，而pycharm2018.1.1之前的版本都是按照旧版pip执行安装，安装东西时可能报错。

(2)安装后端所需环境

```
    pip install -r requirements.txt
```

#### 2、ES
- [ElasticSearch](https://www.elastic.co/cn/downloads/past-releases/elasticsearch-5-5-3)：5.5.3
  运行时如果报错
- [ik分词器](https://github.com/medcl/elasticsearch-analysis-ik/releases/tag/v5.5.3):5.5.3
 （ES和ik版本必须一致，否则会报错）
- ElasticSearch Head 插件(如果可以科学上网，直接在应用商店添加；不能的话可以把插件拖到扩展程序中，这里有好多个[Chrome插件下载的网址](https://zhuanlan.zhihu.com/p/35802469),比如https://www.crx4chrome.com/，下载插件后自己百度安装教程，一般拖到Google的扩展程序里就可以了。
#### 3、前端 
[node.js下载](https://nodejs.org/zh-cn/download/)

(1)在terminal中执行以下命令，安装前端所需依赖:
```
    // 打开前端目录
    cd appfront
    // 安装前端所需依赖
    npm install
```
(2)运行以及打包

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

## 三、Problem:
#### 2019/5/3

1.错误： elasticsearch5.5.3启动失败，出现如下提示：
```
Java HotSpot(TM) 64-Bit Server VM warning: INFO: os::commit_memory(0x0000000085330000, 2060255232, 0) failed; 
error='Cannot allocate memory' (errno=12)
```
由于elasticsearch5.0默认分配jvm空间大小为2g，修改jvm空间分配

打开ElasticSearch/config/jvm.options
```
-Xms2g
-Xmx2g
```
修改为
```
-Xms512m
-Xmx512m
```
##### 2019/5/4：

1.redis部分
问题：redis_cli.zincrby("hot_search", key_words)在es6.7.0下报错缺少value 
  
解决：加入增量，redis_cli.zincrby("hot_search",1,key_words)

2.在python3中，关于redis读取数据带有‘b’的问题

问题：存进去的是字符串类型的数据，取出来却是字节类型的，这是由于python3的与redis交互的驱动的问题，Python2取出来的就是字符串类型的。

解决：加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。

##### 2019/5/5:

1.ES版本问题！！！ 

问题：
```
  elasticsearch.exceptions.RequestError: 
  TransportError(400, 'invalid_type_name_exception', 
  "Document mapping type name can't start with '_', found: [_suggest]")
```
解决：搜索提示部分出错，将本地ES降级到5.5.3，同时要下载同版本的ik分词器




