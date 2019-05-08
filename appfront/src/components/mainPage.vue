<template>
  <div class="container">
    <!--顶部搜索框-->
    <div class="my_header">
      <search-box @notifyQuery="handleQuery"></search-box>
    </div>
    <div class="my_body">
      <!--左侧信息源-->
      <div class="my_left">
        <data_source></data_source>
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
          allDatas:[], // 搜索到的全部数据
          movies: [], // 当前页面信息
          total: 0, // 条目总数
          page_nums: 0, // 总页数
          page_size: 8, // 每页条目数量
          currentPage: 0, //当前页面
          hot_search: [],  //热门搜索
          activeIndex: '1', //当前激活菜单
          menuContent: ["全部","喜剧","科幻","动画","恐怖片"]
        }
      },
      methods:{
          // 初次创建时获取所有的数据
          fetchData(){
            this.init()
            getSomeMovies().then(response =>{
                this.allDatas = response.response_datas
                this.hot_search = response.hot_search
                this.buildMovieInfo(this.allDatas,this.page_size)
            }).catch(error =>{
              console.log(error)
            })
          },
          // 创建本页面的信息
          buildMovieInfo(){
            this.total = this.allDatas.length
            this.page_nums = Math.ceil(this.total / this.page_size)
            this.currentPage = 1
            if(this.page_size > 0){
              this.movies = this.allDatas.slice(0,Math.min(this.page_size,this.total))
            }
          },
          // 如果页码变化，改变页面的显示数据
          handleCurrentChange(){
            this.movies = this.allDatas.slice((this.currentPage-1) * this.page_size,Math.min(this.currentPage* this.page_size,this.total))
          },
          // 如果每页容量发生变化，需要重新构建首页
          handleSizeChange(val) {
            this.currentPage = 0
            this.page_size = val
            this.buildMovieInfo()
          },
          // 建立查询
          handleQuery(query){
            this.init()
            getSearchMovies({s:query })
              .then(response =>{
                this.allDatas = response.all_hits
                this.hot_search = response.hot_search
                let msg1 = "查询到" +  this.allDatas.length + "条电影信息"
                let msg2 = "无匹配的电影信息"
                // 若匹配的数据不为空，进行一些页面的初始化
                if(this.allDatas.length > 0){
                   this.$message({
                      message: msg1,
                      type: 'success',
                      duration: 1600,
                      showClose: true
                    });
                  this.buildMovieInfo()
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
          // 初始化页面信息
          init(){
            this.allDatas = []
            this.movies = []
            this.total = 0
            this.currentPage = 0
          },
          // 选中的菜单变化时
          handleSelect(key, keyPath) {
            this.activeIndex = key
            if(key === '1' || key === 1)
              this.fetchData()
            else
              this.handleQuery(this.menuContent[key-1])
          },
          // 响应热门搜索的点击事件
          handleHotClick(hot_query){
            this.activeIndex = '1'
            this.handleQuery(hot_query)
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
