<template>
    <div class="info">
      <el-card>
      <img  class="image" :src="getImages(dataSet.image_url)">
      <div>
        <span><a :href="dataSet.movie_url">{{getFirstTitle(dataSet.title)}}</a></span>
        <el-rate
          v-model="dataSet.star"
          disabled
          show-score
          :allow-half="true"
          text-color="#ff9900"
          score-template="{value}"
          :colors="['#99A9BF', '#F7BA2A', '#FF9900']">
        </el-rate>
      </div>
      </el-card>
    </div>
</template>

<script>
export default {
  name: 'movieInfo',
  data () {
    return {
      rate: 3.7
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
      console.log(titles)
      return titles[0]
    },
    dealStar(star){
      return parseFloat(star)/2
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
    width: 115px;
    height: 160px;
  }
</style>
