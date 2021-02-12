def mapquest_data_scraper(url, source_phone):
    print(space)
    print(url)
    new_data_list = []
    validated = False
    try:
        driver.get("https://" + url)
    except:
        raw_input("Driver isn't working properly. Press Enter to continue")
        driver.get("https://" + url)
    html_page = driver.page_source
    page_soup = soup(html_page, 'html.parser')
    try:
        error_container = page_soup.find("body", {"class": "error-page"})
        if "WHOOPS!" in error_container.text:
            print("error page")
    except:
        pass
    try:
        company_name = page_soup.find(
            "div", {"class": "header-wrapper"}).text.strip()
    except:
        company_name = ""
    else:
        try:
            company_name = string_cleaner(company_name)
            print("Company Name: " + company_name)
        except:
            pass
    try:
        email = page_soup.find("email", {"class": "ng-scope"})
        email = email.find("a", {"class": "ng-scope"}
                           )["href"].replace("mailto:", "")
        email = string_cleaner(email)
        print("Email: " + email)
    except:
        email = ""
    try:
        reviews = page_soup.find(
            "span", {"class": "numerals ng-binding"}).text.strip().replace(" Reviews", "")
        reviews = string_cleaner(reviews)
        print("Reviews: " + reviews)
    except:
        reviews = ""
    try:
        stars = page_soup.find("meta", {"itemprop": "ratingValue"})
        stars = stars.text.strip()
        stars = string_cleaner(stars)
        print("Rating: " + stars)
    except:
        stars = ""
    try:
        claimed_container = page_soup.find("span", {"id": "verified-business"})
        claimed = claimed_container.text.strip()
        claimed = string_cleaner(claimed)
        print("Claimed: " + claimed)
    except:
        claimed = ""
    try:
        cc_payment = page_soup.find("li", {"itemprop": "paymentAccepted"})
        cc_payment = cc_payment.text.strip()
        cc_payment = string_cleaner(cc_payment)
        print("Accepted Payment: " + cc_payment)
    except:
        cc_payment = ""
    try:
        phone_number = page_soup.find(
            "p", {"ng-if": "ctrl.getPhone()"}).text.strip()
        phone_number = remove_phone_format(phone_number)
        print("Phone Number: " + phone_number)
        if phone_number == source_phone:
            validated = True
    except:
        phone_number = ""
    print("Validated: " + str(validated))
    new_data_list.append(company_name)
    new_data_list.append(email)
    new_data_list.append(reviews)
    new_data_list.append(stars)
    new_data_list.append(claimed)
    new_data_list.append(cc_payment)
    new_data_list.append(phone_number)
    new_data_list.append(validated)
    return new_data_list
