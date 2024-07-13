from seleniumwire import webdriver
from os import getenv
from dotenv import load_dotenv

load_dotenv()
DRIVER_PATH = getenv("SELENIUM_DRIVER_PATH")

driver = webdriver.Chrome(DRIVER_PATH)
