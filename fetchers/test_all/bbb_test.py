from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from fetchers.test_all.url_scrapers.bbb_url_and_phone_scraper import bbb_url_and_phone_scraper


firefox_options = Options()
firefox_options.headless = True
driver = webdriver.Firefox(
    executable_path="/usr/local/share/geckodriver", options=firefox_options)
driver.set_page_load_timeout(60)

vertical, location = "garage door repair", "02333"
print(bbb_url_and_phone_scraper(driver, vertical, location))
