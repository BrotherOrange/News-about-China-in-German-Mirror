# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

client = pymongo.MongoClient()
collection = client["itcast"]["person"]

class FirstPipeline:
    def process_item(self, item, spider):
        item["hello"] = 'world'
        # print(item)
        return item

class FirstPipeline1:
    def process_item(self, item, spider):
        collection.insert_one(item)
        print(item)
        return item
