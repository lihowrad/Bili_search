# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    CONTENT = scrapy.Field()
    SENDING_TIME = scrapy.Field()
    UID = scrapy.Field()

class BVSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    BV_NUMBER = scrapy.Field()

