from ..items import cover
from scrapy import Spider
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from scrapy_selenium import SeleniumRequest
from PIL import Image


class CoverSpider(Spider):
    name = "comickSpider"
    custom_settings = {"USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

    def __init__(self, start_url, first_chapter, last_chapter, *args, **kwargs):
        super(CoverSpider, self).__init__(*args, **kwargs)
        self.all_image_paths = {}
        self.first_chapter = first_chapter
        self.last_chapter = last_chapter
        self.start_url = f"{start_url}?page={0}&lang=en&group={1}"
        self.page = 1

        yield SeleniumRequest(start_url + "?page=1&lang=en", callback=self.pre_parse)

    # we're starting from the last page, as we want to 
    def pre_parse(self, response):
        last_page = response.find_elements_by_xpath("//nav[@aria-label='pagination']/a")[-1]
        last_page = last_page.get_attribute('href')
        self.page = int(last_page.split('&')[0][-1])

        self.group = response.find_elements_by_xpath("//tbody")[2]
        self.group = self.group.find_elements_by_xpath(".//tr[1]")[0].text
        self.group = self.group.split('\n')[-1]

        yield SeleniumRequest(self.start_url.format(self.page, self.group), callback=self.parse)

    def parse(self, response):
        chapters = response.xpath("//tbody")[2]
        chapters = chapters.find_elements_by_xpath(".//tr")

        # get the first and last chapter, see if it falls in the range that we want
        latest_page_chapter = chapters[0].xpath(".//a/@href").get().split('-')
        oldest_page_chapter = chapters[-1].xpath(".//a/@href").get().split('-')

        # if it doesn't, then go to the next page and keep checking
        if int(latest_page_chapter) > self.first_chapter:
            self.page -= 1
            yield SeleniumRequest(self.start_url.format(self.page, self.group), callback=self.parse)

        # now that we're in the right page, visit the link for the first chapter till the last chapter
        # and download the chapter
        pages = response.find_elements_by_xpath("//tbody")[2]
        for page in pages:
            pages = page.find_element_by_xpath(".//tr/td/a").text
            int(pages[4:-5])
        

        # some code that'll help later
        # links = []
        # for chapter in chapters:
        #     link = chapter.find_element_by_xpath(".//a").get_attribute('href')
        #     if link.split('-')[-1] == 'en':
        #         links.append(link)

        