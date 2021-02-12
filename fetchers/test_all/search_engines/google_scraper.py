from bs4 import BeautifulSoup as soup

from fetchers.test_all.utils.search_engine_utils import (browser_phone_translater,
                                                         source_url_filter,
                                                         valid_domain_check)


def google_scraper(driver, phone_number, pages_per_search_engine):
    blocked = False
    google_results = []
    # pages_per_search_engine = pages_per_search_engine + 1
    pages_per_search_engine = pages_per_search_engine*10
    translated_phone = browser_phone_translater(phone_number)
    search_url = 'https://www.google.com/search?q=' + \
        translated_phone + '&num=' + str(pages_per_search_engine)
    try:
        driver.get(search_url)
    except Exception as e:
        print(e)
        return []
    html_page = driver.page_source
    page_soup = soup(html_page, 'html.parser')
    result_containers = page_soup.findAll("div", {"class": "yuRUbf"})
    if "Our systems have detected unusual traffic" in page_soup.text:
        blocked = True
    for container in result_containers:
        for link in container.find_all('a'):
            link = link.get('href')
            link = str(link)
            valid_domain = valid_domain_check(link)
            if valid_domain:
                valid_url = source_url_filter(link)
                if valid_url:
                    if 'https' in link:
                        link = link.split('https://')[-1]
                        link = link.split('+')[0]
                        link = link.split('&')[0]
                    if '?' in link:
                        link = link.split('?')[0]
                    if '%' in link:
                        pass
                    else:
                        if link in google_results:
                            pass
                        else:
                            google_results.append(link)
                            # print("google ---> " + link)
    return google_results, blocked
