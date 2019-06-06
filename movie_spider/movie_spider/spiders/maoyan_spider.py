# -*- coding: utf-8 -*-
import scrapy
from .. import items
from scrapy.selector import Selector
from scrapy.http import Request
from urllib.parse import urljoin


class MaoyanSpiderSpider(scrapy.Spider):
    name = 'maoyan_spider'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def parse(self, response):
        maoyan_item = items.MaoYanMoviesItem()
        selector = Selector(response)
        Movies = selector.xpath('//dd')
        for eachMovie in Movies:
            title = eachMovie.xpath('div[@class="channel-detail movie-item-title"]/a/text()').extract()[0]
            image_url = eachMovie.xpath('div[@class="movie-item"]//div[@class="movie-poster"]/img[2]/@data-src').extract()[0]
            if len(image_url) == 0:
                image_url = eachMovie.xpath('div[@class="movie-item"]//div[@class="movie-poster"]/img[2]/@src').extract()[0]
            print(image_url)
            movie_url = eachMovie.xpath('div[@class="channel-detail movie-item-title"]/a/@href').extract()[0]
            movie_star1 = eachMovie.xpath('div[@class="channel-detail channel-detail-orange"]/i[@class="integer"]/text()').extract_first("")
            movie_star2 = eachMovie.xpath('div[@class="channel-detail channel-detail-orange"]/i[@class="fraction"]/text()').extract_first("")

            maoyan_item['title'] = title
            maoyan_item['star'] = movie_star1 + movie_star2
            maoyan_item['movie_url'] = "https://maoyan.com" + movie_url
            maoyan_item['image_url'] = image_url
            maoyan_item['movieInfo'] = ''
            maoyan_item['quote'] = ''
            # 需要将数据yield到pipelines里面去
            print(maoyan_item)
            yield maoyan_item
            # # 解析下一页的规则，取的后一页的xpath
        next_link = selector.xpath("//div[@class='movies-pager']/ul/li[last()]/a/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield Request(url=urljoin(response.url, next_link), callback=self.parse)

