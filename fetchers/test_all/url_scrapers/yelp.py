from fetchers.test_all.utils.duplicate_checker import duplicate_checker
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as soup


# def create_driver():
#     firefox_options = Options()
#     firefox_options.headless = True
#     driver = webdriver.Firefox(
#         executable_path="/usr/local/share/geckodriver", options=firefox_options)
#     driver.set_page_load_timeout(30)
#     return driver


def yelp_url_scraper_test(driver, vertical, location):
    url_list = set()

    yelp_url = f"https://www.yelp.com/search?find_desc={vertical}&find_loc={location}&start=0"

    try:
        driver.get(yelp_url)
        html_page = driver.page_source
        with open("aver.html", "w+") as f:
            f.write(html_page)
        page_soup = soup(html_page, 'html.parser')
        no_result_container = page_soup.find(
            "div", {"class": "display--inline-block__09f24__FsgS4 margin-b1__09f24__1647o border-color--default__09f24__R1nRO"})
        no_result_container_2 = page_soup.find(
            "h3", {"class": "heading--h3__09f24__2-flz"})
        if no_result_container:
            no_result = no_result_container.text.strip()
            if "Suggestions for improving" in no_result:
                return []
        if no_result_container_2:
            no_result = no_result_container_2.text.strip()
            if "We're sorry, the page of results you requested is unavail" in no_result:
                return []
        lead_container = page_soup.findAll(
            'div', {'class': 'container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__1H_WE border--right__09f24__28idl border--bottom__09f24__2FjZW border--left__09f24__33iol border-color--default__09f24__R1nRO'})
        # print(lead_container)
    except Exception as e:
        print(e)
        # driver.close()
        return []

    repeat = set()
    for lead in lead_container:
        for link in lead.find_all('a'):
            link = link.get('href')
            link = str(link)
            if '/biz/' in link:
                link = link.replace('/biz', 'www.yelp.com/biz')
                link = link.split("?")[0]
                link = link.split('.com')[1]
                link = "www.yelp.com" + link
                # print(link)
                status = duplicate_checker("yelp url", link)
                if status:
                    url_list.add(link)
                else:
                    repeat.add(link)

    result_count = len(url_list) + len(repeat)

    page_urls = []
    try:
        page_count_container = page_soup.find(
            "div", {"aria-label": "Pagination navigation"})
        page_count_container = page_count_container.find(
            "span", {"class": "css-e81eai"})
        if not page_count_container:
            return page_urls

        page_count = int(page_count_container.text.strip().split()[-1])

        for page_number in range(page_count):
            page_urls.append(
                f"https://www.yelp.com/search?find_desc={vertical}&find_loc={location}&start={page_number * result_count}")

    except Exception as e:
        print(e)
    finally:
        # driver.close()
        return page_urls


# print(yelp_url_scraper_test(create_driver(), "plumbing", "91496"))
