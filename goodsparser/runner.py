import sys
sys.path.append("..")
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Lesson_7_Selenium_in_Scrapy.goodsparser import settings
from Lesson_7_Selenium_in_Scrapy.goodsparser.spiders.leroymerlin import LeroymerlinSpider



if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(LeroymerlinSpider, search=sys.argv[1])
    process.crawl(LeroymerlinSpider, search='кресло')


    process.start()