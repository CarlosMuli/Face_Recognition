# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class InsightCrawlerPipeline(object):
    def process_item(self, item, spider):
        item['images'] = item['images'][0]['path'].replace('full/', '')	# Isolates the .jpg file from images
        return item
