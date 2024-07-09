# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class cover(Item):
    title = Field()
    image_urls = Field()

class chap_images(Item):
    image_urls = Field()
    chapter = Field()
