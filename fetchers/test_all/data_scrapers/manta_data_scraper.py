def manta_data_scraper(url, source_phone):
    driver_2 = webdriver.Chrome(chrome_options=chrome_options)
    import json
    print(space)
    new_data_list = []
    validated = False
    url = "https://" + url
    print(url)
    website = ""
    try:
        driver_2.get(url)
    except:
        raw_input("Driver isn't working properly press Enter to continue.")
        driver_2.get(url)
    html_page = driver_2.page_source
    page_soup = soup(html_page, 'html.parser')
    if "Access denied" in page_soup.text:
        print("Blocked")
    if "One more step" in page_soup.text:
        raw_input("Captcha")
    try:
        claimed = page_soup.find("div", {
                                 "class": "inline-block mt-1 rounded-r bg-gray-light h-7 px-2 py-1 text-xs text-gray-dark"}).text.strip().lower()
        claimed = string_cleaner(claimed)
        print("Claimed: " + claimed)
    except:
        claimed = ""
    one = page_soup.find("script", type="application/ld+json")
    two = str(one).split('<script type="application/ld+json">')[1]
    three = two.split('</script>')[0]
    json_snippet = json.loads(three)
    try:
        company_name = json_snippet["name"]
        company_name = string_cleaner(company_name)
        print("Company Name: " + company_name)
    except:
        company_name = ""
    try:
        phone_number = json_snippet["telephone"]
        phone_number = remove_phone_format(phone_number)
        if phone_number == source_phone:
            validated = True
        print("Phone Number: " + phone_number)
    except:
        phone_number = ""
    try:
        email_address = json_snippet["email"]
        email_address = string_cleaner(email_address)
        if "null" in email_address:
            email_address = ""
        else:
            print("Email: " + email_address)
    except:
        email_address = ""
    try:
        street_address = str(json_snippet["address"]["streetAddress"][0])
        street_address = string_cleaner(street_address)
        print("Street: " + street_address)
    except:
        street_address = ""
    try:
        city = str(city["address"]["addressLocality"][0])
        city = string_cleaner(city)
        print("City: " + city)
    except:
        city = ""
    try:
        state = str(json_snippet["address"]["addressRegion"])
        state = string_cleaner(state)
        print("State: " + state)
    except:
        state = ""
    try:
        zip_code = str(json_snippet["address"]["postalCode"])
        zip_code = string_cleaner(zip_code)
    except:
        zip_code = ""
    else:
        print("Zip Code: " + zip_code)
    try:
        country = str(country["address"]["addressCountry"][0])
        country = string_cleaner(country)
        print("Country: " + country)
    except:
        country = ""
    try:
        contact_name = str(json_snippet["employee"]["givenName"])
        contact_name = string_cleaner(contact_name)
        print("First Name: " + contact_name)
    except:
        contact_name = ""
    try:
        contact_last_name = str(json_snippet["employee"]["familyName"])
        contact_last_name = string_cleaner(contact_last_name)
        print("Last Name: " + contact_last_name)
    except:
        contact_last_name = ""
    try:
        contact_title = json_snippet["employee"]["jobTitle"]
        contact_title = string_cleaner(contact_title)
        print("Title: " + contact_title)
    except:
        contact_title = ""
    try:
        num_employees = str(json_snippet["numberOfEmployees"])
        num_employees = string_cleaner(num_employees)
        print("Employees: " + num_employees)
    except:
        num_employees = ""
    try:
        years = int(json_snippet["foundingDate"])
        years = datetime.now().year-years
        years = string_cleaner(years)
        print("Years in business: " + str(years))
    except:
        years = ""
    try:
        stars = str(json_snippet["aggregateRating"]["ratingValue"])
        stars = string_cleaner(stars)
        print("Rating: " + stars)
    except:
        stars = ""
    try:
        reviews = str(json_snippet["aggregateRating"]["reviewCount"])
        reviews = string_cleaner(reviews)
        print("Reviews: " + reviews)
    except:
        try:
            reviews = page_soup.find("div", {"class": "mbm"})
            reviews = reviews.find("a").text.split(" ")[0]
            reviews = string_cleaner(reviews)
            print("Reviews: " + reviews)
        except:
            reviews = ""
    try:
        website_l = json_snippet["sameAs"]
        try:
            if isinstance(website_l, list):
                for w in website_l:
                    website = website + \
                        str(w).replace("http://", "").replace("www.",
                                                              "").replace("https://", "") + " "
                    website = string_cleaner(website)
            else:
                website = str(website_l).replace(
                    "http://", "").replace("www.", "").replace("https://", "")
                website = string_cleaner(website)
        except:
            pass
    except:
        website = ""
    else:
        if "null" in website:
            website = ""
        else:
            print("Website : " + website)
    try:
        category_container = page_soup.find(
            "div", {"class": "text-gray-400 text-sm py-3 hidden lg:block"})
        category_container = category_container.text.strip()
        category = category_container.split("\n")[-1]
        string_cleaner(category)
        print("Category: " + category)
    except:
        category = ""
    print("Validated: " + str(validated))
    driver_2.close()
    new_data_list.append(claimed)
    new_data_list.append(company_name)
    new_data_list.append(phone_number)
    new_data_list.append(email_address)
    new_data_list.append(street_address)
    new_data_list.append(city)
    new_data_list.append(state)
    new_data_list.append(zip_code)
    new_data_list.append(contact_name)
    new_data_list.append(contact_last_name)
    new_data_list.append(contact_title)
    new_data_list.append(num_employees)
    new_data_list.append(years)
    new_data_list.append(stars)
    new_data_list.append(reviews)
    new_data_list.append(website)
    new_data_list.append(category)
    new_data_list.append(validated)
    return new_data_list
