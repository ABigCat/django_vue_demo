<template>
  <div class="container">
    <div class="my_header">
      <search-box @notifyQuery="handleQuery"></search-box>
    </div>
    <div class="my_body">
      <div class="my_left">
        <data_source></data_source>
      </div>
      <div class="my_main">
        <div class="movie_box">
          <div  v-for="(item,index) in this.movies" :key="index">
            <movie-info :dataSet="item"></movie-info>
          </div>
        </div>
      </div>
      <div class="my_aside">
        <top_search :data-set="hot_search"></top_search>
      </div>
    </div>
    <div class="my_footer">
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-size="page_size"
          :page-sizes="[4,6,8,10,20]"
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
          allDatas:[],
          movies: [],
          total: 0,
          page_nums: 0, // 总页数
          page_size: 8, // 每页条目数量
          currentPage: 0, //
          hot_search: []
        }
      },
      methods:{
          // 初次创建时获取所有的数据
          fetchData(){
            getSomeMovies().then(response =>{
                console.log(response.response_datas)
                this.allDatas = response.response_datas
                this.buildMovieInfo(this.allDatas,this.page_size)
            }).catch(error =>{
              console.log(error)
            })
          },
          // 创建本页面的信息
          buildMovieInfo(){
            console.log(this.allDatas[0])
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
          // 如果每页容量发生变化
          handleSizeChange(val) {
            console.log(`每页 ${val} 条`)
            console.log(val);
            this.currentPage = 0
            this.page_size = val
            this.buildMovieInfo()
          },
          // 建立查询
          handleQuery(query){
            this.init()
            getSearchMovies({s:query })
              .then(response =>{
                console.log(1)
                console.log("myresponse:" + response)
                this.allDatas = response.all_hits
                this.hot_search = response.hot_search
                console.log("allDatas" + this.allDatas)
                console.log("hot_search:" + this.hot_search)
                let msg1 = "查询到" +  this.allDatas.length + "条电影信息"
                let msg2 = "无匹配的电影信息"
                console.log(2)
                // 若匹配的数据不为空，进行一些页面的初始化
                if(this.allDatas.length > 0){
                   this.$message({
                      message: msg1,
                      type: 'success'
                    });
                  this.buildMovieInfo()
                } else {
                  this.$message({
                      message: msg2,
                      type: 'info'
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
    border-bottom: solid 1px #c0ccda;
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
