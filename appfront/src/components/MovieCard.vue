<template>
  <div>
      <el-card>
        <div class="cardBox">
          <img  class="image" :src="getImages(dataSet.image_url)">
          <div class="details">
            <div><a :href="dataSet.movie_url">{{dataSet.title}}</a></div>
            <div>{{dataSet.movieInfo[0]}}</div>
            <el-rate
              v-model="(dataSet.star/2).toFixed(1)"
              disabled
              show-score
              :allow-half="true"
              text-color="#ff9900"
              score-template="{value}"
              :colors="['#99A9BF', '#F7BA2A', '#FF9900']">
            </el-rate>
          </div>
        </div>

      </el-card>
    </div>
</template>

<script>
    export default {
        name: "MovieCard",
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
  .cardBox{
     height: 145px;
    display: flex;
    flex-direction: row;
  }
  .image{
    width: 75px;
    height: 107px;
  }
  .details{
    display: flex;
    flex-direction: column;
    align-content: space-around;
    justify-content: flex-start;
  }
</style>
