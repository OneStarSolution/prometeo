import time

from bs4 import BeautifulSoup as soup

from fetchers.test_all.utils.duplicate_checker import duplicate_checker


def bbb_url_and_phone_scraper(driver, vertical, location):

    if location.isdigit():
        country = "USA"
    else:
        country = "CAN"
    bbb_url_list = []
    bbb_phone_list = []
    new_lead_dict_list = []
    already_clicked = False
    bbb_domain = {"domain": "https://www.bbb.org/search?find_country=",
                  "country": "USA", "mid_string": "&find_loc=",
                  "location": "85033", "mid_string_2": "&find_text=",
                  "vertical": "plumbing", "end_string": "&page=", "page": "1"}
    for page in range(1, 50):  # Default value is 17
        bbb_url = bbb_domain["domain"] + country + bbb_domain["mid_string"] + location + \
            bbb_domain["mid_string_2"] + vertical + \
            bbb_domain["end_string"] + str(page)

        try:
            driver.get(bbb_url)
            if not already_clicked:
                try:
                    time.sleep(1.5)
                    xp = "/html/body/div[2]/div[3]/div/form/div[2]/fieldset/div[1]/label[2]/div/p"
                    elem = driver.find_element_by_xpath(xp)
                    if elem:
                        elem.click()
                except Exception as e:
                    print(e)
                    pass
                else:
                    already_clicked = True

                if not already_clicked:
                    try:
                        time.sleep(1.5)
                        xp = "/html/body/div[4]/div[3]/div/form/div[2]/fieldset/div[1]/label[2]/div/span/span[1]/input"
                        elem = driver.find_element_by_xpath(xp)
                        if elem:
                            elem.click()
                            time.sleep(1)
                    except Exception as e:
                        print(e)
                        pass
                    else:
                        already_clicked = True

            html_page = driver.page_source
            page_soup = soup(html_page, 'html.parser')

            no_result_container = page_soup.find(
                "h2", {"class": "MuiTypography-root search-no-results__title MuiTypography-h2"})

            if no_result_container:
                no_result = no_result_container.text.strip()
                if "sorry, we found no results" in no_result:
                    print("[*] No more results, moving to next location")
                    break
                if "Sin resultado" in no_result:
                    print("[*] No more results, moving to next location")
                    break
            lead_container = page_soup.findAll(
                'div', {'class': 'Content-ro0uyh-0 VyFaZ rresult-item-ab__content'})
        except Exception as e:
            print(e)
            continue

        for lead in lead_container:
            new_lead_dict = {}
            link = ""
            phone_number = ""
            source_url = ""
            for link in lead.find_all('a'):
                link = link.get('href')
                link = link.encode('ascii', 'ignore')
                link = str(link)
                if '/profile/' in link and 'bbb.org' in link:
                    source_url = link
                    source_url = source_url.split("https://")[1]
                    if '?' in source_url:
                        source_url = source_url.split("?")[0]
                if 'tel' in link:
                    try:
                        phone_number = link.split("+")[1]
                        phone_number = phone_number[2:]
                        phone_number = phone_number.replace("-", "")
                    except Exception as e:
                        print(e)
                        phone_number = " "
            if source_url in bbb_url_list:
                pass
            else:
                if phone_number in bbb_phone_list:
                    pass
                else:
                    url_status = duplicate_checker('bbb url', source_url)
                    if url_status:
                        status = duplicate_checker('phone', phone_number)
                        if status:
                            bbb_url_list.append(source_url)
                            bbb_phone_list.append(phone_number)
                            new_lead_dict["bbb url"] = source_url
                            new_lead_dict["phone"] = phone_number
                            new_lead_dict_list.append(new_lead_dict)
    return(new_lead_dict_list)
