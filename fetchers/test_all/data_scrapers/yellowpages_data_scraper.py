from bs4 import BeautifulSoup as soup

from fetchers.test_all.utils.clean_utils import string_cleaner, remove_phone_format


space = "*" * 75


def yellowpages_data_scraper(driver, url, source_phone):
    if url[-1].isdigit():
        print(url)
    else:
        extra_string = url.split("/")[-1]
        extra_string = "/" + extra_string
        url = url.replace(extra_string, "")
        print(url)
    print(space)
    validated = False
    new_data_list = []
    try:
        driver.get("https://" + url)
        html_page = driver.page_source
        page_soup = soup(html_page, 'html.parser')
        body = page_soup.find("body").text.strip()
    except Exception as e:
        print(e)
        return
    try:
        body = page_soup.find("body").text.strip()
        if "Forbidden" in body:
            print("Forbidden, Please change IP an press Enter")
    except Exception as e:
        print(e)
        pass
    try:
        company_name = page_soup.find("div", {"class": "sales-info"})
        company_name = company_name.text.strip()
        company_name = string_cleaner(company_name)
        if 'add to favorites' in company_name:
            company_name = company_name.split('add to favorites')[0]
        print("Company Name: " + company_name)
    except Exception as e:
        print(e)
        company_name = ""

    phone_number = ""
    rating = ""

    try:
        phone_number = page_soup.find("p", {"class": "phone"})
        phone_number = phone_number.text.strip()
        phone_number = remove_phone_format(phone_number)
        if phone_number == source_phone:
            validated = True
        print("Phone Number: " + phone_number)
    except Exception as e:
        print(e)
        phone = ""
    try:
        rating_containers = page_soup.findAll(
            "meta", {"property": "og:description"})
        for rating_container in rating_containers:
            rating_container = str(rating_container)
            if 'stars' in rating_container:
                rating = rating_container.split(" stars on YP")[0]
                rating = rating.replace('<meta content="Rated ', "")
                rating = string_cleaner(rating)
                print("Rating: " + rating)
                break
            else:
                rating = ""
    except Exception as e:
        print(e)
        rating = ""
    try:
        street_address = str(page_soup.find(
            "script", {"type": "application/ld+json"}))
        street_address = street_address.split('streetAddress":"')[1]
        street_address = street_address.split('"')[0]
        street_address = string_cleaner(street_address)
        print("Street Address: " + street_address)
    except Exception as e:
        print(e)
        street_address = ""
    try:
        city = str(page_soup.find("script", {"type": "application/ld+json"}))
        city = city.split('addressLocality":"')[1]
        city = city.split('"')[0]
        city = string_cleaner(city)
        print("City: " + city)
    except Exception as e:
        print(e)
        city = ""
    try:
        state = str(page_soup.find("script", {"type": "application/ld+json"}))
        state = state.split('addressRegion":"')[1]
        state = state.split('"')[0]
        state = string_cleaner(state)
        print("State: " + state)
    except Exception as e:
        print(e)
        state = ""
    try:
        zip_code = str(page_soup.find(
            "script", {"type": "application/ld+json"}))
        zip_code = zip_code.split('postalCode":"')[1]
        zip_code = zip_code.split('"')[0]
        zip_code = string_cleaner(zip_code)
        print("Zip Code: " + zip_code)
    except Exception as e:
        print(e)
        zip_code = ""
    try:
        email_address = page_soup.find(
            "div", {"class": "business-card-footer"})
        email_address = str(email_address)
        email_address = email_address.split('mailto:')[1]
        email_address = email_address.split('"')[0]
        email_address = string_cleaner(email_address)
        print("Email: " + email_address)
    except Exception as e:
        print(e)
        email_address = ""
    try:
        years_container = page_soup.find("div", {"class": "number"})
        years = years_container.text.strip()
        years = string_cleaner(years)
        print("Years in business " + years)
    except Exception as e:
        print(e)
        years = ""
    try:
        reviews = str(page_soup.find(
            "script", {"type": "application/ld+json"}))
        reviews = reviews.split('reviewCount":')[1]
        reviews = reviews.split('}')[0]
        reviews = string_cleaner(reviews)
        print("Reviews: " + reviews)
    except Exception as e:
        print(e)
        reviews = ""
    try:
        website = str(page_soup.find(
            "script", {"type": "application/ld+json"}))
        website = website.split('"&nbsp;http://')[1]
        website = website.split('&nbs')[0]
        website = string_cleaner(website)
        print("Website " + website)
    except Exception as e:
        print(e)
        website = ""
    try:
        temp_phone_list = []
        extra_phone_container = page_soup.find("dd", {"class": "extra-phones"})
        extra_phone_container = extra_phone_container.findAll("span")
    except Exception as e:
        print(e)
        alt_phone_1 = ""
        alt_phone_2 = ""
    else:
        for p_number in extra_phone_container:
            p_number = p_number.text.strip()
            if ") " in p_number:
                temp_phone_list.append(p_number)
        alt_phone_1 = temp_phone_list[0]
        alt_phone_1 = remove_phone_format(alt_phone_1)
        if alt_phone_1 == source_phone:
            validated = True
        try:
            alt_phone_2 = temp_phone_list[1]
            alt_phone_2 = remove_phone_format(alt_phone_2)
        except Exception as e:
            print(e)
            alt_phone_2 = ""
        if alt_phone_2 == source_phone:
            validated = True
        print("Alt Phone Number 1: " + alt_phone_1 +
              '\n' + "Alt Phone Number 2: " + alt_phone_2)
    try:
        category_container = page_soup.find("dd", {"class": "categories"})
        category_container = category_container.text.strip()
        category_container = category_container.split(',')
    except Exception as e:
        print(e)
        category_1 = ""
        category_2 = ""
    else:
        try:
            category_1 = category_container[0]
            category_1 = string_cleaner(category_1)
            print("Category 1: " + category_1)
        except Exception as e:
            print(e)
            category_1 = ""
        try:
            category_2 = category_container[1]
            category_2 = string_cleaner(category_2)
            print("Category 2: " + category_2)
        except Exception as e:
            print(e)
            category_2 = ""
    try:
        accepted_payment = page_soup.find(
            "dd", {"class": "payment"}).text.strip()
        accepted_payment = string_cleaner(accepted_payment)
        print("Accepted Payment: " + accepted_payment)
    except Exception as e:
        print(e)
        accepted_payment = ""
    try:
        aka = page_soup.find("dd", {"class": "aka"}).text.strip()
        aka = string_cleaner(aka)
        print("Alias: " + aka)
    except Exception as e:
        print(e)
        aka = ""
    try:
        business_info = page_soup.find("section", {"id": "business-info"})
        business_info = str(business_info)
        # print(business_info)
        if 'mailto' in business_info:
            alt_email = business_info.split('mailto:')[1]
            alt_email = alt_email.split('"')[0]
            alt_email = string_cleaner(alt_email)
            print("Alt Email: " + alt_email)
        else:
            alt_email = ""
    except Exception as e:
        print(e)
        alt_email = ""
    print("Validated: " + str(validated))
    try:
        new_data_list.append(company_name)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(phone_number)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(rating)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(street_address)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(city)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(state)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(zip_code)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(email_address)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(years)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(reviews)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(website)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(alt_phone_1)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(alt_phone_2)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(category_1)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(category_2)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(accepted_payment)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(aka)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    try:
        new_data_list.append(alt_email)
    except Exception as e:
        print(e)
        new_data_list.append("error")
    new_data_list.append(validated)
    return new_data_list
