<template>
  <div class="menu_box">
    <el-menu :default-active="activeIndex" class="el-menu-demo"
             mode="horizontal"
             background-color="#D1EEEE"
             @select="handleSelect">
       <el-menu-item v-for="(item,i) in menuContent" :index=item :key="i">{{item}}</el-menu-item>
     </el-menu>
    <div class="table_box">
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="order" label="排名" width="160"></el-table-column>
        <el-table-column prop="star" label="评分" width="160"></el-table-column>
        <el-table-column  label="电影名称" width="260">
          <template slot-scope="scope">
            <a href="scope.row.movie_url">{{scope.row.title}}</a>
          </template>
        </el-table-column>
        <el-table-column  prop="movie_info" label="电影详情" >
        </el-table-column>
     </el-table>
    </div>
  </div>

</template>

<script>
    export default {
        name: "topPage",
      data(){
          return{
            menuContent: ["首页","豆瓣电影Top250","猫眼Top100"],
            activeIndex: "豆瓣电影Top250",
            tableData: []
          }
      },
      methods:{
          handleSelect(key, keyPath){
            console.log("key:" + key)
            console.log("keypath:" + keyPath)
            if(key == "首页"){
              this.$router.push("/")
            }
          }
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
