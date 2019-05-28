import request from '@/utils/request'
/**
 * date：2019.4.16
 * author:liqian
 * description：
 */

export function getSomeMovies(params) {
  return request({
    url: '/test',
    method: 'get',
    params
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
