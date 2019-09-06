# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InsightCrawlerItem(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    position = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    #pass

    
