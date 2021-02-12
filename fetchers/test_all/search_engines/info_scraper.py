from bs4 import BeautifulSoup as soup

from fetchers.test_all.utils.search_engine_utils import (browser_phone_translater,
                                                         source_url_filter,
                                                         valid_domain_check)


def info_scraper(driver, phone_number, pages_per_search_engine):
    blocked = False
    info_results = []
    pages_per_search_engine = pages_per_search_engine + 1
    for i in range(1, pages_per_search_engine):
        translated_phone = browser_phone_translater(phone_number)
        search_url = 'https://www.info.com/serp?q=' + \
            translated_phone + '&page=' + str(i)

        try:
            driver.get(search_url)
            html_page = driver.page_source
            page_soup = soup(html_page, 'html.parser')
            no_result_container = page_soup.find(
                "div", {"class": "notice-noresults-empty"})
            no_result_container = no_result_container.text.strip()
            if 'No search results' in no_result_container:
                break
            html_string = (str(page_soup))
            html_string = html_string.split("</head>")[1]
            page_soup = soup(html_string, 'html.parser')
            blocked_check = page_soup.find("div", {"class": "error-code"})
            blocked_check = blocked_check.text.strip()

            try:
                if 'ERR_EMPTY' in blocked_check:
                    blocked = True
            except Exception as e:
                blocked = True
            result_containers = page_soup.findAll(
                "div", {"class": "web-google__result"})

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
                            if '?' in link:
                                link = link.split('?')[0]
                            if '%' in link:
                                pass
                            else:
                                if link in info_results:
                                    pass
                                else:
                                    info_results.append(link)
                                    # print("info ---> " + link)

        except Exception as e:
            pass

    return info_results, blocked
