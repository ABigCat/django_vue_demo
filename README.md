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
- ElasticSearch：6.7.0
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

[spider项目创建以及运行]

[django项目创建以及运行]

[vue项目创建以及运行]




