from pydantic import HttpUrl
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


target_url = "https://www.manta.com/c/mmlkg64/bob-s-oil-burner-service"


class MantaFetcherController:
    def __init__(self, url: HttpUrl) -> None:
        firefox_options = Options()
        firefox_options.headless = True
        self.driver = webdriver.Firefox(
            executable_path="/usr/local/share/geckodriver", options=firefox_options)
        self.url_base = url

    def _read_web(self):
        self.driver.get(self.url_base)
        return self.driver.page_source

    def __del__(self):
        print("closing driver...")
        self.driver.close()
