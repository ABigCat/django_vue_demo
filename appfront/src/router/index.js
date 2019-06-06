import Vue from 'vue'
import Router from 'vue-router'
import homePage from '@/components/homePage'
import mainPage from '@/components/mainPage'
import topPage from '@/components/topPage'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: homePage
    },
    {
      path: '/main',
      name: 'mainPage',
      component: mainPage
    },
    {
      path: '/top',
      name: 'topPage',
      component: topPage
    }
  ]
})
