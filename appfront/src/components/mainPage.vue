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
        <top_search></top_search>
      </div>
    </div>
    <div class="my_footer">
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-size="8"
          layout="total, prev, pager, next"
          :total="info_size">
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
          info_size: 0,
          currentPage: 1
        }
      },
      methods:{
          fetchData(){
            getSomeMovies().then(response =>{
                console.log(response.response_datas)
                this.allDatas = response.response_datas
                this.buildMovieInfo(this.allDatas,8)
            }).catch(error =>{
              console.log(error)
            })
          },
          fetchQueryInfo(query){
            console.log('query:' + query)
           // getSearchMovies({q:query})
           //   .then(response =>{
           //     this.movies = response.all_hits
           //   }).catch(error =>{
           //     console.log(error)
           // })
          },
          buildMovieInfo(all_Info, page_size){
            this.info_size = all_Info.length
            this.page_size = Math.ceil(this.info_size / 8)
            this.currentPage = 1
            if(this.page_size > 0){
              this.movies = all_Info.slice(0,Math.min(page_size,this.info_size))
            }
          },
          handleCurrentChange(){
            // console.log('this.currentPage :' + this.currentPage)
            this.movies = this.allDatas.slice((this.currentPage-1) * 8,Math.min(this.currentPage* 8,this.info_size))
            // console.log('this.movies :' + this.movies)
          },
          handleQuery(query){
            // console.log(query)
            getSearchMovies({s:query })
              .then(response =>{
                this.allDatas = response.all_hits
                msg1 = "查询到" +  this.allDatas.length + "电影信息"
                msg2 = "无匹配的电影信息"
                if(this.allDatas.length > 0){
                   this.$message({
                      message: msg1,
                      type: 'success'
                    });
                  this.buildMovieInfo(this.allDatas,8)
                } else {
                  this.movies = []
                  this.page_size = 1
                  this.info_size = 0
                  this.$message({
                      message: msg2,
                      type: 'info'
                    });
                }
              }).catch(error =>{
                console.log(error)
            })
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
