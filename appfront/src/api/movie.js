import request from '@/utils/request'
/**
 * date：2019.4.16
 * author:liqian
 * description：
 */

export function getSomeMovies() {
  return request({
    url: '/test',
    method: 'get'
  })
}
export function getSuggestMovies(params) {
  return request({
    url: '/suggest',
    method: 'get',
    params
  })
}
export function getSearchMovies(params) {
  return request({
    url: '/search',
    method: 'get',
    params
  })
}
