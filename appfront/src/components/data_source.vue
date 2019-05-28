<template>
     <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="text1">数据源</span>
        <!--<el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>-->
      </div>
       <!--:class="{ 'active': item == this.currentValue}"-->
      <div v-for="(item, index) in dataSources" :key="index"  @click="clickDataSource(item)" class="text item" >
        {{item}}
      </div>
    </el-card>
</template>

<script>
    export default {
        name: "data_source",
        props:{
          dataSources:{
            type: Array,
            default: ()=>[]
          }
          // currentValue:{
          //   type: String,
          //   default: "豆瓣top250"
          // }
        },
        methods:{
          clickDataSource(index){
            this.$emit("onDataSourceChange",item);
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
  }

  .item {
    margin-bottom: 18px;
  }
  .box-card {
    height: 400px;
  }
  .active {

  }

</style>
