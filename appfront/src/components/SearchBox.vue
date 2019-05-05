<template>
    <div class="search-box">
      <img class="logo" src="@/assets/logo.jpg">
      <div class="input_box">
         <!--<el-input placeholder="请输入内容" v-model="query" >-->
          <!--<el-button slot="append" icon="el-icon-search" @click="notifyQuery">搜索</el-button>-->
         <!--</el-input>-->
        <el-autocomplete
            class="inline-input"
            v-model="query"
            :fetch-suggestions="querySearch"
             placeholder="请输入想要搜索的电影"
            :trigger-on-focus="false"
            @select="handleSelect">
          <el-button slot="append" icon="el-icon-search" @click="notifyQuery">搜索</el-button>
        </el-autocomplete>
    </div>
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
           console.log(response)
           cb(response.res_data)
       }).catch(error=>{
         console.log(error)
       })
      },
      handleSelect(item) {
        console.log(item);
        this.query = item.value
        this.notifyQuery()
      },
      notifyQuery(){
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
  .input_box{
    width:80%;
    padding: 10px;
  }
  .logo{
    width: 150px;
    height: 60px;
  }
</style>
