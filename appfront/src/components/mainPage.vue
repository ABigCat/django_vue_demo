<template>
  <div class="container">
    <!--顶部搜索框-->
    <div class="my_header">
      <search-box @notifyQuery="handleQuery"></search-box>
    </div>
    <div class="my_body">
      <!--左侧信息源-->
      <div class="my_left">
        <data_source :data-sources="data_source" @onDataSourceChange="handleDataSourceChange"></data_source>
      </div>
      <div class="my_main">
        <!--菜单-->
        <div>
           <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
             <el-menu-item v-for="(item,i) in menuContent" :index="getIndex(i)">{{item}}</el-menu-item>
           </el-menu>
        </div>
        <!--电影信息-->
        <div class="movie_box">
          <div  v-for="(item,index) in this.movies" :key="index">
            <movie-info :dataSet="item"></movie-info>
          </div>
        </div>
      </div>
      <!--右侧热门搜索-->
      <div class="my_aside">
        <top_search :data-set="hot_search" @notifyClick="handleHotClick"></top_search>
      </div>
    </div>
    <!--底部分页-->
    <div class="my_footer">
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-size="page_size"
          :page-sizes="[4,5,6,8,10,20]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
      </el-pagination>
    </div>
  </div>
</template>

<script>
    import SearchBox from "./SearchBox";
    import MovieInfo from "./movieInfo";
    import { getSomeMovies, getSearchMovies} from "@/api/movie"
    import Data_source from "./data_source";
    import Top_search from "./top_search";
    export default {
      name: "mainPage",
      components: {Top_search, Data_source, MovieInfo, SearchBox},
      data(){
        return{
          movies: [], // 当前页面信息，
          total: 0, // 条目总数
          page_nums: 0, // 总页数
          page_size: 8, // 每页条目数量
          currentPage: 1, //当前页面
          hot_search: [],  //热门搜索
          activeIndex: '1', //当前激活菜单
          menuContent: ["全部","喜剧","科幻","动画","恐怖片"],
          data_source:["豆瓣top250","测试1","测试2", "测试3"],
          search_content:''
        }
      },
      methods:{
          // 初次创建时获取所有的数据,初始时根据页面激活的菜单和每页条目数量获取如下数据
          // movies：前几条数据
          // total: 总条数
          // page_nums: 总页数
          // hot_search: 热门搜索

          fetchData(){
            this.search_content = ''
            getSomeMovies({currentPage: this.currentPage, page_size: this.page_size}).then(response =>{
                this.movies = response.response_datas
                this.hot_search = response.hot_search
                this.page_nums = response.page_nums
                this.total = response.total_nums
            }).catch(error =>{
              console.log(error)
            })
          },
          fetchSearchData(){
             getSearchMovies({currentPage: this.currentPage, page_size: this.page_size,s:this.search_content })
              .then(response =>{
                this.hot_search = response.hot_search
                this.total = response.total_nums
                this.page_nums = response.page_nums
                let msg1 = "查询到" +  this.total + "条电影信息"
                let msg2 = "无匹配的电影信息"
                // 若匹配的数据不为空，进行一些页面的初始化
                if(this.movies.length > 0){
                  if(this.currentPage === 1 || this.currentPage ==="1"){
                    this.$message({
                      message: msg1,
                      type: 'success',
                      duration: 1600,
                      showClose: true
                    });
                  }
                  this.movies = response.all_hits
                } else {
                  this.$message({
                      message: msg2,
                      type: 'info',
                      duration: 1600,
                      showClose: true
                    });
                }
              }).catch(error =>{
                console.log(error)
            })
          },
          // 如果页码变化，改变页面的显示数据
          handleCurrentChange(){
            console.log('currentPage:' + this.currentPage)
            this.handleTwoQuery()
          },
          // 处理在有无查询条件两种情况下的请求
          handleTwoQuery(){
            // 若查询内容不为空
            if(!!this.search_content){
              this.fetchSearchData()
            } else {
              this.fetchData()
            }
          },
          // 如果每页容量发生变化，需要重新构建首页
          handleSizeChange(val) {
            this.currentPage = 1
            this.page_size = val
            this.handleTwoQuery()
          },
          // 建立查询
          handleQuery(query){
            this.search_content = query
            if(!!query){
              this.activeIndex = '1'
              this.fetchSearchData()
            }
            else
               this.$message({
                      message: "请输入搜索内容",
                      type: 'warning',
                      duration: 1600,
                      showClose: true
                    })
          },
          // 选中的菜单变化时
          handleSelect(key, keyPath) {
            this.activeIndex = key
            if(key == '1' || key == 1) {
              this.search_content = ''
            } else {
              this.search_content = this.menuContent[key-1]
            }
            this.currentPage = 1
            this.handleTwoQuery()

          },
          // 响应热门搜索的点击事件
          handleHotClick(hot_query){
            this.activeIndex = '1'
            this.search_content = hot_query
            this.currentPage = 1
            this.fetchSearchData()
          },
          // 响应数据源的变化
          handleDataSourceChange(data_source){
            // 重新发起查询请求，获取当前数据源的查询结果
            console.log("data_source:" + data_source)
          },
          // 返回菜单的index（string类型）
          getIndex(i){
            return i + 1 + ""
          }
      },
      created(){
         this.fetchData()
      }
    }
</script>

<style scoped>
  .movie_box{
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
  }
  .my_header{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 10%;
    min-height: 100px;
    /*border-bottom: solid 1px #c0ccda;*/
    /*background-color: #c0ccda;*/
  }
  .my_body{
    height: 80%;
    min-height: 400px;
    display: flex;
    flex-direction: row;
    /*background-color: #13ce66;*/
  }
   .my_left{
     width: 15%;
     height: 70%;
     min-width: 100px;
     min-height: 400px;
     /*border: solid 1px #cccccc;*/
     margin: 10px;
     background-color: white;
     /*background-color: #c0ccda;*/
  }
  .my_main{
     width: 70%;
     height: 70%;
    min-height: 400px;
    /*border: solid 1px #cccccc;*/
     margin: 10px;
     background-color: white;
    /*background-color: #f0c78a;*/
  }
  .my_aside{
     width: 15%;
     height: 70%;
     min-height: 400px;
     /*border: solid 1px #cccccc;*/
     margin: 10px;
     background-color: white;
    /*background-color: #c0ccda;*/
  }
  .my_footer{
    height: 80px;
    /*background-color: #00ffff;*/
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .container{
    background-color: #f6f6f6;
  }
</style>
