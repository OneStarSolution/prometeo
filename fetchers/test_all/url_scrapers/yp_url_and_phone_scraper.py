import re

from bs4 import BeautifulSoup as soup

from fetchers.test_all.utils.duplicate_checker import duplicate_checker


def yp_url_and_phone_scraper(driver, vertical, location):
    yp_url_list = []
    yp_phone_list = []
    new_lead_dict_list = []
    yp_domain = {"domain": "https://www.yellowpages.com/search?search_terms=",
                 "vertical": "plumbing",
                 "mid_string": "&geo_location_terms=",
                 "location": "85033", "end_string": "&page=", "page": "1"}
    for page in range(1, 16):  # set to 99, changed to 5 for testing purposes
        yp_url = yp_domain["domain"] + vertical + yp_domain["mid_string"] + \
            location + yp_domain["end_string"] + str(page)

        try:
            print(f"trying to get: {yp_url}")
            driver.get(yp_url)

            html_page = driver.page_source

            page_soup = soup(html_page, 'html.parser')
            lead_container = page_soup.find(
                "div", {"class": "search-results organic"})
            if lead_container is None:
                # print("[*] No more results, moving to next location")
                break
        except Exception as e:
            print(e)
            pass
        else:
            lead_container = lead_container.findAll("div", {"class": "v-card"})
            for lead in lead_container:
                new_lead_dict = {}
                link = ""
                phone_number = " "
                source_url = ""
                for link in lead.find_all('a'):
                    link = link.get('href')
                    link = str(link)
                    if '/mip/' in link:
                        source_url = link
                        source_url = "www.yellowpages.com" + \
                            source_url.split("?")[0]
                        if source_url[-1].isdigit():
                            pass
                        else:
                            extra_string = source_url.split("/")[-1]
                            extra_string = "/" + extra_string
                            source_url = source_url.replace(extra_string, "")
                            print(source_url)
                        break
                try:
                    phone_number = lead.find(
                        "div", {"class": "phones phone primary"})
                    phone_number = phone_number.text.strip()
                    phone_number = re.sub("[^0-9]", "", phone_number)
                    phone_number = phone_number.encode('ascii', 'ignore')
                    # print(phone_number)
                except Exception as e:
                    print(e)
                    phone_number = ""
                if source_url in yp_url_list:
                    pass
                else:
                    if phone_number in yp_phone_list:
                        pass
                    else:
                        url_status = duplicate_checker('yp url', source_url)
                        if url_status:
                            status = duplicate_checker('phone', phone_number)
                            if status:
                                yp_url_list.append(source_url)
                                yp_phone_list.append(phone_number)
                                new_lead_dict["yp url"] = source_url
                                new_lead_dict["phone"] = phone_number
                                new_lead_dict_list.append(new_lead_dict)

    return new_lead_dict_list
