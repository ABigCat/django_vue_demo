<template>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="text1">热门搜索</span>
        <!--<el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>-->
      </div>
      <div v-for="(item, index) in dataSet" :key="index" class="text item">
        <el-button :type="getRandomColor()" round @click="hotClick(index)">{{item[0]}}</el-button>
      </div>
    </el-card>
</template>

<script>
    export default {
        name: "top_search",
        data(){
          return{
            colorSet:["primary","success","warning","danger","info"]
          }
        },
        props:{
           dataSet:{
            type: Array,
            default: () => []
          }
        },
        methods:{
          getRandomColor(){
            // [0,5)
            let index = Math.floor(Math.random()*5)
            return this.colorSet[index]
          },
          hotClick(index){
            this.$emit("notifyClick",this.dataSet[index][0])
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
