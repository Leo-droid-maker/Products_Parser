# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient, ASCENDING
from pymongo.errors import *


class GoodsparserPipeline:

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client.goods_from_scrapy

    def process_item(self, item, spider):
        # print()

        collection = self.mongobase[spider.name]
        collection.create_index([("url", ASCENDING)], name="goods_url_index", unique=True)
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print(f'Данный элемент уже есть в базе данных: {item["name"]}')

        return item


class GoodsImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for image in item['images']:
                try:
                    yield Request(image)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['images'] = [i[1] for i in results if i[0]]
        return item
