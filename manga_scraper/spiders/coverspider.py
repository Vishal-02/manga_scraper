from ..items import cover
from scrapy import Spider
from scrapy import signals
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from PIL import Image
import json

# i want to use the spider to scrape the bookmarks of my mangakakalot account
# so that i can populate the database. I can do this with just selenium, but scrapy's
# just faster and i wanna try it out
class CoverSpider(Spider):
    name = "bookmark_scraper"
    custom_settings = {"USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

    def start_requests(self):
        url = "https://manganato.com/"
        bkm_url = "https://manganato.com/bookmark"
        
        # i want to use the selenium webdriver to go to the bookmarks page
        # using the cookies i give it to log in.

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--enable-cookies")
        
        driver = webdriver.Chrome(
            "../../chromedriver-win64/chromedriver.exe",
            options=chrome_options
        )

        driver.get(url)

        with open("manga_cookies.json", "r") as file:
            cookies = json.load(file)

        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()
        yield SeleniumRequest(
            url=bkm_url,
            callback=self.parse,
        )

    def parse(self, response):
        print(response.body)

# this is the spider i used to scrape asurascans, i'll keep it here for the reference
# but now i'm trying to use selenium and all to link my database to it as well
# so i rename this spider and the one i actually want to use is above
class _CoverSpider(Spider):
    name = "pyimagesearch-cover-spider"
    start_urls = ["https://asurascans.us/read-en-us/the-return-of-the-disaster-class-hero/chapter-0/"]
    custom_settings = {"USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

    def __init__(self, name: str | None = None, **kwargs: Image.Any):
        super().__init__(name, **kwargs)
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
        pages = response.xpath("//img[starts-with(@id, 'image-')]/@data-src").getall()

        for page in pages:
            self.image_downloaded += 1
            url = page.strip("\n\t")
            self.all_image_paths.append(f"images/full/{url.split('/')[-1]}")
            self.printThree(self.all_image_paths)
            yield cover(image_urls=[url])


