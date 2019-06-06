<template>
    <div class="search-box">
      <!--<img class="logo" src="@/assets/logo.jpg">-->
        <el-autocomplete
            class="inline-input"
            v-model="query"
            :fetch-suggestions="querySearch"
             placeholder="请输入想要搜索的电影"
            :trigger-on-focus="false"
            @select="handleSelect"
            :highlight-first-item="true">
          <el-button type="primary" slot="append" icon="el-icon-search" @click="notifyQuery">搜索</el-button>
        </el-autocomplete>
    </div>
</template>

<script>
  import {getSearchMovies, getSuggestMovies} from "../api/movie";
  export default {
  name: 'SearchBox',
  data () {
    return {
      query: '',
      searchArr: []
    }
  },
  methods:{
     querySearch(queryString, cb) {
       getSuggestMovies({ s: queryString})
         .then(response =>{
           cb(response.res_data)
       }).catch(error=>{
         console.log(error)
       })
      },
      handleSelect(item) {
        this.query = item.value
        this.notifyQuery()
      },
      notifyQuery(){
        if(this.query === "")
            this.$message('请输入搜索内容')
        else
          this.$emit('notifyQuery',this.query)
      }
  }


}
</script>

<style scoped>
  .search-box{
    width: 60%;
    display: flex;
    flex-direction: row;
    padding: 20px;
    justify-content: center;
  }
  .inline-input{
    width: 600px;
  }
  .logo{
    width: 150px;
    height: 60px;
  }
</style>
