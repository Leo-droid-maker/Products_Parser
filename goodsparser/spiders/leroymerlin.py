import sys
sys.path.append("..")
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from Lesson_7_Selenium_in_Scrapy.goodsparser.items import GoodsparserItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):

        next_page_link = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
        # links = response.xpath('//a[contains(@data-qa, "product-image")]/@href').getall()
        links = response.xpath('//a[contains(@data-qa, "product-image")]')
        for link in links:
            yield response.follow(link, callback=self.product_parse)

    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=GoodsparserItem(), response=response)
        loader.add_xpath('name', '//h1[@slot="title"]/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('images', '//source[@media=" only screen and (min-width: 1024px)"]/@data-origin')

        yield loader.load_item()

        # name = response.xpath('//h1[@slot="title"]/text()').get()
        # link = response.url
        # price = response.xpath('//span[@slot="price"]/text()').get()
        # images = response.xpath('//source[@media=" only screen and (min-width: 1024px)"]/@data-origin').getall()
        # item = GoodsparserItem(name=name, link=link, price=price, images=images)
        # yield item

