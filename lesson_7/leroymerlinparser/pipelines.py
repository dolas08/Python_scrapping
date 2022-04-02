# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
# from scrapy.pipelines.files import IPipeline
import os
from urllib.parse import urlparse


class LeroymerlinparserPipeline:
    def process_item(self, item, spider):
        # print()
        return item


class LeroymerlinparserPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for photo in item['photos']:
                try:
                    yield scrapy.Request(photo)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        asd = item['url'].replace('https://www.castorama.ru/', '') + '/'
        return f'{asd}' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):

        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
