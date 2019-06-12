<template>
  <div class="menu_box">
    <el-menu :default-active="movie_origin" class="el-menu-demo"
             mode="horizontal"
             background-color="#D1EEEE"
             @select="handleSelect">
       <el-menu-item v-for="(item,index) in menuContent" :index=index :key="index">{{item}}</el-menu-item>
     </el-menu>
    <div class="table_box">
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="movie_order" label="排名" width="100" align="center"></el-table-column>
        <el-table-column prop="star" label="评分" width="100" align="center"></el-table-column>
        <el-table-column  label="电影名称" width="260" align="center">
          <template slot-scope="scope">
            <a href="scope.row.movie_url" style="color: #c00">{{scope.row.title}}</a>
          </template>
        </el-table-column>
        <el-table-column  prop="movie_info" label="电影详情" align="center">
        </el-table-column>
     </el-table>
    </div>
  </div>

</template>

<script>
    import {getTopMovies} from "../api/movie";
    export default {
        name: "topPage",
      data(){
          return{
            menuContent: ["首页","豆瓣电影Top250","猫眼Top100"],
            tableData: [],
            movie_origin: 1
          }
      },
      methods:{
          handleSelect(key, keyPath){
            if(key === "0" || key === 0){
              this.$router.push("/")
            } else {
              this.movie_origin = key
              this.fetchTableData();
            }
          },
          fetchTableData(){
            getTopMovies({ "movie_origin": this.movie_origin})
              .then(response =>{
              this.tableData = response.result
            }).catch(error => {
              console.log(error)
            })
          }
      },
      created() {
          this.fetchTableData()
      }
    }
</script>

<style scoped>
  .menu_box{
    width: 70%;
    padding-left: 15%;
    padding-top: 20px;
  }
  .table_box{
    padding-top: 40px;
  }
</style>
