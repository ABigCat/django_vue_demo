# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from .. import items
from urllib.parse import urljoin

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    # redis_key = 'douban:start_urls'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        item = items.MovieSpiderItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="item"]')
        # .xpath() 及 .css() 方法返回一个类 SelectorList 的实例,
        #  它是一个新选择器的列表。这个API可以用来快速的提取嵌套数据。
        for eachMovie in Movies:
            title = eachMovie.xpath('div[@class="info"]/div[@class="hd"]/a/span/text()').extract()  # 多个span标签
            fullTitle = "".join(title)  # 将多个字符串无缝连接起来
            movieInfo = eachMovie.xpath('div[@class="info"]/div[@class="bd"]/p/text()').extract()
            star = eachMovie.xpath('div[@class="info"]/div[@class="bd"]/div[@class="star"]/span/text()').extract()[0]
            quote = eachMovie.xpath('div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            image_url = eachMovie.xpath('div[@class="pic"]//img/@src').extract()[0]
            movie_url = eachMovie.xpath('div[@class="pic"]//a/@href').extract()[0]

            # quote可能为空，因此需要先进行判断
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fullTitle
            item['movieInfo'] = movieInfo
            item['star'] = star
            item['quote'] = quote
            item['image_url'] = image_url
            item['movie_url'] = movie_url
            yield item
        nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
        # 第10页是最后一页，没有下一页的链接
        if nextLink:
            nextLink = nextLink[0]
            yield Request(url=urljoin(response.url, nextLink), callback=self.parse)