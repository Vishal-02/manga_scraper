# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class CustomPipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        self.images_downloaded = 0
        self.all_image_paths = []

    def printThree(self, text):
        print(f"\n\n\n{text}\n\n\n")

    def file_path(self, request, response=None, info=None, *, item=None):
        remove = ['?', '/', '%', '»', '«']
        name = "".join([i for i in item['title'] if i not in remove])

        return f"full/{name}.jpg"
    


