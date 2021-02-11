from bs4 import BeautifulSoup as soup

from fetchers.test_all.utils.duplicate_checker import duplicate_checker


def yelp_url_scraper(driver, vertical, location):
    url_list = []
    yelp_domain = {"domain": "https://www.yelp.com/search?find_desc=", "vertical": "plumbing",
                   "mid_string": "&find_loc=", "location": "85033", "end_string": "&ns=1&start="}
    for page in range(17):  # default value is 17 here
        directory_page = page*10
        yelp_url = yelp_domain["domain"] + vertical + yelp_domain["mid_string"] + \
            location + yelp_domain["end_string"] + str(directory_page)
        # print(space + '\n' + yelp_url)

        try:
            driver.get(yelp_url)
            html_page = driver.page_source
            page_soup = soup(html_page, 'html.parser')
            no_result_container = page_soup.find(
                "div", {"class": "display--inline-block__09f24__FsgS4 margin-b1__09f24__1647o border-color--default__09f24__R1nRO"})
            no_result = no_result_container.text.strip()
            if "Suggestions for improving" in no_result:
                # print("[*] No more results, moving to next location")
                break
            lead_container = page_soup.findAll(
                'div', {'class': 'container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__1H_WE border--right__09f24__28idl border--bottom__09f24__2FjZW border--left__09f24__33iol border-color--default__09f24__R1nRO'})

        except Exception as e:
            print(e)
            continue

        for lead in lead_container:
            for link in lead.find_all('a'):
                link = link.get('href')
                link = str(link)
                if '/biz/' in link:
                    link = link.replace('/biz', 'www.yelp.com/biz')
                    link = link.split("?")[0]
                    link = link.split('.com')[1]
                    link = "www.yelp.com" + link
                    if link in url_list:
                        pass
                    else:
                        status = duplicate_checker("yelp url", link)
                        if status:
                            url_list.append(link)
                            break
    return(url_list)
