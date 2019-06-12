# -*- coding: utf-8 -*-
import scrapy
from .. import items
from scrapy.selector import Selector
from scrapy.http import Request
from urllib.parse import urljoin


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4']

    def parse(self, response):
        maoyan_item = items.MaoYanMoviesItem()
        selector = Selector(response)
        Movies = selector.xpath('//dd')
        for eachMovie in Movies:
            order = eachMovie.xpath('i/text()').extract()[0]
            title = eachMovie.xpath('a/@title').extract()[0]
            movie_url = eachMovie.xpath('a/@href').extract()[0]

            image_url = eachMovie.xpath('a/img[2]/@src').extract()
            if len(image_url) == 0:
                image_url = eachMovie.xpath('a/img[2]/@data-src').extract()
            print(image_url[0])
            movie_star1 = eachMovie.xpath('div[@class="board-item-main"]//i[@class="integer"]/text()').extract_first("")
            movie_star2 = eachMovie.xpath('div[@class="board-item-main"]//i[@class="fraction"]/text()').extract_first("")
            movie_info = eachMovie.xpath('div[@class="board-item-main"]//p[@class="star"]/text()').extract_first("")

            maoyan_item["order"] = order
            maoyan_item['title'] = title
            maoyan_item['star'] = movie_star1 + movie_star2
            maoyan_item['movie_url'] = "https://maoyan.com" + movie_url
            maoyan_item['image_url'] = image_url
            maoyan_item['movie_info'] = movie_info.replace(" ", "").replace("\n", "")
            maoyan_item['movie_origin'] = '2'
            # 需要将数据yield到pipelines里面去
            print(maoyan_item)
            yield maoyan_item
            # # 解析下一页的规则，取的后一页的xpath
        next_link = selector.xpath("//div[@class='pager-main']/ul/li[last()]/a/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield Request(url=urljoin(response.url, next_link), callback=self.parse)

