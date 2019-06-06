<template>
    <div class="query_box">
      <search-box @notifyQuery="handleQuery"></search-box>
      <el-tag type="warning" @click="handleTogglePage">豆瓣电影Top250/猫眼Top100</el-tag>
    </div>
</template>

<script>
    import SearchBox from "./SearchBox";
    export default {
      name: "homePage",
      components: {SearchBox},
      methods:{
          handleQuery(query){
            // 跳转页面向mainPage
            this.$router.push({
              name: "mainPage",
              params:{
                searchContent: query
              }
            })
          },
        handleTogglePage(){
            // 跳转页面向topPage
          this.$router.push('top')
        }
      }
    }
</script>

<style scoped>
  .query_box{
    height: 600px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
