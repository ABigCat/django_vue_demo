<template>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="text1">热门搜索</span>
        <!--<el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>-->
      </div>
      <div v-for="(item, index) in dataSet" :key="index" class="text item">
        {{item}}
      </div>
    </el-card>
</template>

<script>
    export default {
        name: "top_search",
        props:{
           dataSet:{
            type: Array,
            default: () => []
          }
        }
    }
</script>

<style scoped>
    .text1{
        font-weight: bold;
  }
.text {
    font-size: 14px;
    font-weight: bold;
  }

  .item {
    margin-bottom: 18px;
  }
   .box-card {
    height: 400px;
  }

</style>
