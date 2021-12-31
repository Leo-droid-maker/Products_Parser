# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def clear_price(value):
    value = value.replace(' ', '')
    try:
        return int(value)
    except Exception:
        return value



class GoodsparserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    url = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    _id = scrapy.Field()
