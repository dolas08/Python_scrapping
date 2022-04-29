# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaItem(scrapy.Item):
    # define the fields for your item here like:
    # user_id = scrapy.Field()
    # username = scrapy.Field()
    _id = scrapy.Field()
    post_data = scrapy.Field()






