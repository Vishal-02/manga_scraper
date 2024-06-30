from urllib.parse import urljoin
from scrapy import Spider
from scrapy import signals
from scrapy.http import Request
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
import sqlite3
from ..items import cover

# i want this to go to a specific chapter in comick and make it a pdf
# it needs to do this for some specific number of chapters
# i'll need to integrate selenium with this one for it to work without any hitches,
# won't be possible otherwise
class TitleSpider(Spider):
    name = "titleImageSpider"
    start_urls = ["https://mangakakalot.com"] # you'll have to append /comic/some_code for it to go to a chapter
    custom_settings = {"USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        chromedriver_path = "..\..\..\web_scraping\chromedriver-win64\chromedriver.exe"
        self.driver = webdriver.Chrome(chromedriver_path, options=options)

    def print_three(self, data):
        print(f"\n\n\n{data}\n\n\n")

    def find_most_similar(self, title, options):
        title = title.split()
        similar = 0
        final_link = None
    
        for name, link in options:
            if similar == 0:
                final_link = link
                continue

            temp = [i for i in title if i in name.split()]
            if len(temp) > similar:
                final_link = link
                similar = len(temp)

        return final_link

    def get_title_image(self, response, s_name):
        image_url = response.xpath("//span[@class='info-image']/img/@src").get()
        if image_url is None:
            image_url = response.xpath("//div[@class='manga-info-pic']/img/@src").get()

        yield cover(title=s_name, image_urls=[image_url])

    def parse(self, response):
        self.driver.get(response.url)
        con = sqlite3.connect("comick.db")
        cur = con.cursor()
        
        data = cur.execute("SELECT * FROM Manga").fetchall()
        for row in data:
            title, *others = row
            search_bar = self.driver.find_element_by_xpath("//input[contains(@id, 'search_story')]")
            search_bar.send_keys(title)
            search_bar.send_keys(Keys.ENTER)

            anchors = self.driver.find_elements_by_xpath("//h3[contains(@class, 'story_name')]/a")[:10]
            links = [anchor.get_attribute('href') for anchor in anchors]
            names = [anchor.text.lower() for anchor in anchors]

            if len(links) == 0:
                continue

            manga_url = self.find_most_similar(title.lower(), list(zip(names, links)))

            yield Request(url=manga_url, callback=self.get_title_image, cb_kwargs=dict(s_name=title))

        cur.close()
        con.close()