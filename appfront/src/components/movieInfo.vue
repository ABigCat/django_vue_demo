<template>
    <div class="info">
      <el-card shadow="hover">
      <img  class="image" :src="getImages(dataSet.image_url)">
      <div>
        <div>
          <a :href="dataSet.movie_url">{{getFirstTitle(dataSet.title)}}</a>
          <span class="yellowFont">{{dataSet.star}}</span>
        </div>
        <!--<el-rate-->
          <!--v-model="(dataSet.star/2).toFixed(1)"-->
          <!--disabled-->
          <!--show-score-->
          <!--:allow-half="true"-->
          <!--text-color="#ff9900"-->
          <!--score-template="{value}"-->
          <!--:colors="['#99A9BF', '#F7BA2A', '#FF9900']">-->
        <!--</el-rate>-->
        <el-tooltip class="item" effect="dark" :content="dataSet.movieInfo" placement="bottom">
          <el-button type="text" class="button" size="small">电影详情</el-button>
        </el-tooltip>
      </div>
      </el-card>
    </div>
</template>

<script>
export default {
  name: 'movieInfo',
  data () {
    return {
      rate: 3.7,
      myStar: 0
    }
  },
  methods: {
    // 解决403图片缓存问题
    getImages(_url) {
      if (_url !== undefined) {
        let _u = _url.substring(7);
        return 'https://images.weserv.nl/?url=' + _u;
      }
    },
    getFirstTitle(title){
      let titles = title.split('/')
      return titles[0]+"   "
    }
  },
  props:{
    dataSet:{
      type: Object,
      default: ()=>{}
    }
  }
}
</script>

<style scoped>
  .info{
    width: 200px;
    margin: 10px;
  }
  .image{
    width: 105px;
    height: 140px;
  }
  .yellowFont{
    color: #F7BA2A;
  }
</style>
