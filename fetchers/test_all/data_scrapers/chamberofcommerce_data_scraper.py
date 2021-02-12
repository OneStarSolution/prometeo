def chamberofcommerce_data_scraper(url, source_phone):
    import urllib2
    import time
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    validated = False
    new_data_list = []
    print(space)
    url = "https://" + url
    print(url)
    try:
        req = urllib2.Request(url, headers=hdr)
        try:
            page = urllib2.urlopen(req)
        except:
            print("Check your url string and try again")
        else:
            time.sleep(1)
            if page.getcode() != 200:
                print("unsuccessful request")
    except urllib2.HTTPError as e:
        print("error retreiving html")
    else:
        page_soup = soup(page, 'html.parser')
        try:
            company_name = page_soup.find(
                "div", {"class": "profile_business_name"}).text.strip()
            company_name = string_cleaner(company_name)
            print("Company Name: " + company_name)
        except:
            company_name = ""
        try:
            phone_number = page_soup.find(
                "span", {"class": "d-none d-sm-block phone-align"}).text.strip()
            phone_number = phone_number.replace("+1-", "")
            phone_number = remove_phone_format(phone_number)
            if phone_number == source_phone:
                validated = True
            print("Phone Number: " + phone_number)
        except:
            phone_number = ""
        try:
            reviews = page_soup.find(
                "span", {"class": "review_conts_profile"}).text.strip()
            reviews = reviews.replace("(", "")
            reviews = reviews.replace(")", "")
            reviews = string_cleaner(reviews)
            print("Reviews: " + reviews)
        except:
            reviews = ""
        try:
            rating = page_soup.find("div", {"class": "review_rating"})
            rating = str(rating)
            rating = rating.split("data-rateit-value")[1]
            rating = rating.split("data-rateit.ispreset")[0]
            rating = rating.replace('"', '')
            rating = rating.replace('=', '')
            rating = string_cleaner(rating)
            print("Rating: " + rating)
        except:
            rating = ""
        try:
            contact_container = page_soup.find(
                "div", {"class": "about_p_text"})
            contact_container = str(contact_container)
            about_sections = contact_container.split("<br")
            for section in about_sections:
                if 'more information contact' in section:
                    contact_title = section.split(",")[1]
                    contact_name = section.split(",")[0]
                    contact_name = contact_name.split("contact ")[1]
                    contact_name = string_cleaner(contact_name)
                    contact_title = string_cleaner(contact_title)
                    print("Contact Name: " + contact_name +
                          "\nContact Title: " + contact_title)
                    break
                else:
                    contact_name = ""
                    contact_title = ""
        except:
            contact_name = ""
            contact_title = ""
        try:
            breadcrumbs = page_soup.find("ul", {"class": "bredcrump_list"})
            crumbs = breadcrumbs.findAll("li")
            category = crumbs[-2].text.strip()
            category = category.replace(">>", "")
            category = string_cleaner(category)
            print("Category: " + category)
        except:
            category = ""
    print("Validated: " + str(validated))
    new_data_list.append(company_name)
    new_data_list.append(phone_number)
    new_data_list.append(reviews)
    new_data_list.append(rating)
    new_data_list.append(contact_name)
    new_data_list.append(contact_title)
    new_data_list.append(category)
    new_data_list.append(validated)
    return new_data_list
