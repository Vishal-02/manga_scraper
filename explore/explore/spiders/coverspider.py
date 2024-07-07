from ..items import cover
from scrapy import Spider
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from PIL import Image
import json

# this is the spider i used to scrape asurascans, i'll keep it here for the reference
# but now i'm trying to use selenium and all to link my database to it as well
# so i rename this spider and the one i actually want to use is above
class CoverSpider(Spider):
    name = "coverSpider"
    start_urls = ["https://comick.io"]
    custom_settings = {"USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

    def __init__(self, name: str | None = None, **kwargs: Image.Any):
        super().__init__(name, **kwargs)

        # selenium webdriver initialization
        options = Options()
        options.add_argument('--headless')
        chromedriver_path = "..\..\..\web_scraping\chromedriver-win64\chromedriver.exe"
        self.driver = webdriver.Chrome(chromedriver_path, options=options)

        # variables required for the downloading
        self.image_downloaded = 0
        self.all_image_paths = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CoverSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed_handler, signal=signals.spider_closed)
        return spider

    def printThree(self, text):
        print(f"\n\n\n{text}\n\n\n")

    def spider_closed_handler(self, spider):
        if self.image_downloaded > 0:
            self.create_pdf(self.all_image_paths)
            self.image_downloaded = 0 # i'm resetting it for future use, just in case

    def create_pdf(self, image_paths):
        width, _ = Image.open(image_paths[0]).size
        image_one = Image.open(image_paths[0]).convert("RGB")

        self.printThree("We're at create_pdf")

        for i, image in enumerate(image_paths[1:]):
            image = Image.open(image)
            _, height = image.size

            # match the width of the first image, scale the height by the same amount
            factor = width / _
            new_height = int(height * factor)
            image = image.resize((width, new_height))

            image_paths[i + 1] = image

        image_one.save("images/full/result.pdf", save_all=True, append_images=image_paths[1:])

    def parse(self, response):
        # i need to get the chapters first


        pages = None

        for page in pages:
            self.image_downloaded += 1
            url = page.strip("\n\t")
            self.all_image_paths.append(f"images/full/{url.split('/')[-1]}")
            # self.printThree(self.all_image_paths)
            yield cover(image_urls=[url])


