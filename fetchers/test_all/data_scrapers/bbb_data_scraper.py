def bbb_data_scraper(url, source_phone):
    print(space)
    new_data_list = []
    if '?' in url:
        url = url.split("?")[0]
    if 'details' in url:
        pass
    else:
        url = url + '/details'
    url = "https://" + url
    print(url)

    company_name = ""
    phone_number = ""
    city = ""
    state = ""
    zip_code = ""
    street_address = ""
    country = ""
    business_start_date = ""
    first_name = ""
    last_name = ""
    title = ""
    facebook = ""
    twitter = ""
    instagram = ""
    alt_phone = ""
    rating = ""
    review = ""
    claimed = ""
    latitude = ""
    longitude = ""
    validated = False
    phone_list = []
    category_list = []
    try:
        driver.get(url)
    except:
        raw_input(
            "Driver isn't working properly. press enter when ready to Continue")
        driver.get(url)
    try:
        page = driver.page_source
        page_soup = soup(page, 'html.parser')
    except:
        print("Unable to retrieve html")
    else:
        try:
            json_snippet = page_soup.find(
                "script", {"type": "application/ld+json"})
            json_snippet = str(json_snippet).split(
                '<script type="application/ld+json">')[1]
            json_snippet = json_snippet.split('</script>')[0]
            snippet_list = json_snippet.split("],")
            for snippet in snippet_list:
                if 'context' in snippet:
                    main_snippet = snippet.split(",")
                    for value in main_snippet:
                        if "name" in value:
                            company_name = value.split(":")[1]
                            company_name = company_name.replace('"', '')
                            company_name = string_cleaner(company_name)
                            if 'bbb' in company_name:
                                company_name = page_soup.find("title").text
                                company_name = company_name.split(" | ")[0]
                                company_name = string_cleaner(company_name)
                                print(company_name)
                        if "addressLocality" in value:
                            city = value.split(":")[1]
                            city = city.replace('"', '')
                            city = string_cleaner(city)
                        if "addressRegion" in value:
                            state = value.split(":")[1]
                            state = state.replace('"', '')
                            state = string_cleaner(state)
                        if "postalCode" in value:
                            zip_code = value.split(":")[1]
                            zip_code = zip_code.replace('"', '')
                            zip_code = string_cleaner(zip_code)
                            if "-" in zip_code:
                                zip_code = zip_code.split("-")[0]
                        if "streetAddress" in value:
                            street_address = value.split(":")[1]
                            street_address = street_address.replace('"', '')
                            street_address = string_cleaner(street_address)
                        if "addressCountry" in value:
                            country = value.split(":")[1]
                            country = country.replace('"', '')
                            country = string_cleaner(country)
                else:
                    for value in snippet.split(","):
                        if 'foundingDate' in value:
                            business_start_date = value.split(":")[1]
                            business_start_date = business_start_date.replace(
                                '"', '')
                            business_start_date = string_cleaner(
                                business_start_date)
                        if 'givenName' in value:
                            first_name = value.split(":")[1]
                            first_name = first_name.replace('"', '')
                            first_name = string_cleaner(first_name)
                        if 'familyName' in value:
                            last_name = value.split(":")[1]
                            last_name = last_name.replace('"', '')
                            last_name = string_cleaner(last_name)
                        if 'jobTitle' in value:
                            title = value.split(":")[1]
                            title = title.replace('"', '')
                            title = string_cleaner(title)
                        if 'sameAs' in value:
                            website = value.split(":[")[1]
                            website = website.replace('"', '')
                            if '.' not in website:
                                website = ""
                            else:
                                if 'www.' in website:
                                    website = website.split("www.")[1]
                                if '?' in website:
                                    website = website.split("?")[0]
                                if '//' in website:
                                    website = website.split("//")[1]
                            website = string_cleaner(website)
                        if 'latitude' in value:
                            latitude = value.split(":")[1]
                            latitude = latitude.replace('"', '')
                            latitude = string_cleaner(latitude)
                        if 'longitude' in value:
                            longitude = value.split(":")[1]
                            longitude = longitude.replace('"', '')
                            longitude = string_cleaner(longitude)
                        if 'telephone' in value:
                            phone_number = value.split(":")[1]
                            phone_number = phone_number.replace('"', '')
                            phone_number = string_cleaner(phone_number)
                            phone_number = remove_phone_format(phone_number)
                            if phone_number in phone_list:
                                pass
                            else:
                                phone_list.append(phone_number)
            lead_container = page_soup.find(
                'div', {'class': 'MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-3'})
            for lead in lead_container:
                for link in lead.find_all('a'):
                    link = link.get('href')
                    try:
                        link = link.encode('ascii', 'ignore')
                    except:
                        pass
                    link = str(link)
                    if 'tel' in link:
                        try:
                            phone_number = link.split("+")[1]
                            phone_number = phone_number[2:]
                            phone_number = phone_number.replace("-", "")
                            phone_number = remove_phone_format(phone_number)
                            if phone_number in phone_list:
                                pass
                            else:
                                phone_list.append(phone_number)
                        except:
                            pass
                for link in lead.find_all('a'):
                    link = link.get('href')
                    try:
                        link = link.encode('ascii', 'ignore')
                    except:
                        pass
                    link = str(link)
                    if 'facebook.com' in link:
                        facebook = link.lower()
                        if 'www.' in facebook:
                            facebook = facebook.split('www.')[1]
                        break
                for link in lead.find_all('a'):
                    link = link.get('href')
                    try:
                        link = link.encode('ascii', 'ignore')
                    except:
                        pass
                    link = str(link)
                    if 'twitter.com' in link:
                        twitter = link.lower()
                        if 'www.' in twitter:
                            twitter = twitter.split('www.')[1]
                        break
                for link in lead.find_all('a'):
                    link = link.get('href')
                    try:
                        link = link.encode('ascii', 'ignore')
                    except:
                        pass
                    link = str(link)
                    if 'instagram.com' in link:
                        instagram = link.lower()
                        if 'www.' in instagram:
                            instagram = instagram.split('www.')[1]
                        break
            for phone in phone_list:
                phone = remove_phone_format(phone)
                if phone == source_phone:
                    phone_number = phone
                    validated = True
                else:
                    alt_phone = phone
            bbb_meta_data = page_soup.find("script", {"id": "BbbDtmData"})
            bbb_meta_data = str(bbb_meta_data)
            meta_data_list = bbb_meta_data.split(",")
            for i in meta_data_list:
                if 'rating' in i:
                    rating = i.split(":")[1]
                    rating = rating.replace('"', '')
                    rating = string_cleaner(rating)
                if 'accreditedStatus' in i:
                    claimed = i.split(":")[-1]
                    claimed = claimed.replace('"', '')
                    if 'AB' == claimed:
                        claimed = True
                    else:
                        claimed = False
            for lead in lead_container:
                for link in lead.find_all('a'):
                    link = link.get('href')
                    try:
                        link = link.encode('ascii', 'ignore')
                    except:
                        pass
                    link = str(link)
                    if '/category/' in link:
                        category = link.split("/")[-1]
                        category_list.append(category)
        except:
            pass
        print("Company Name: " + company_name)
        print("City: " + city)
        print("State: " + state)
        print("Zip Code: " + zip_code)
        print("Street: " + street_address)
        print("Country: " + country)
        print("Founded Date: " + business_start_date)
        print("First Name: " + first_name)
        print("Last Name: " + last_name)
        print("Title: " + title)
        print("Website: " + website)
        print("Latitude: " + latitude)
        print("Longitude: " + longitude)
        print("Facebook: " + facebook)
        print("Twitter: " + twitter)
        print("Instagram: " + instagram)
        print("Validated Data: " + str(validated))
        print("Phone Number: " + phone_number)
        print("Alt Phone Number: " + alt_phone)
        print("Rating: " + rating)
        print("Review: " + review)
        print("Claimed: " + str(claimed))
        try:
            category_one = category_list[0]
            category_one = category_one.replace("-", " ")
            print("Category One: " + category_one)
        except:
            category_one = ""
        try:
            category_two = category_list[1]
            category_two = category_two.replace("-", " ")
            print("Category Two: " + category_two)
        except:
            category_two = ""
        try:
            category_three = category_list[2]
            category_three = category_three.replace("-", " ")
            print("Category Three: " + category_three)
        except:
            category_three = ""
        new_data_list.append(company_name)
        new_data_list.append(phone_number)
        new_data_list.append(city)
        new_data_list.append(state)
        new_data_list.append(zip_code)
        new_data_list.append(street_address)
        new_data_list.append(country)
        new_data_list.append(business_start_date)
        new_data_list.append(first_name)
        new_data_list.append(last_name)
        new_data_list.append(title)
        new_data_list.append(facebook)
        new_data_list.append(twitter)
        new_data_list.append(instagram)
        new_data_list.append(alt_phone)
        new_data_list.append(rating)
        new_data_list.append(review)
        new_data_list.append(claimed)
        new_data_list.append(latitude)
        new_data_list.append(longitude)
        new_data_list.append(validated)
        new_data_list.append(category_one)
        new_data_list.append(category_two)
        new_data_list.append(category_three)
    return new_data_list
