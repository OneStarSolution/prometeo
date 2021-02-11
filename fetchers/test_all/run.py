import os
import re
import time

import requests
import pandas as pd

from bs4 import BeautifulSoup as soup
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from fetchers.test_all.data_scrapers.yelp_data_scraper import yelp_data_scraper
from fetchers.test_all.url_scrapers.yelp_url_scraper import yelp_url_scraper
from fetchers.test_all.url_scrapers.bbb_url_and_phone_scraper import bbb_url_and_phone_scraper
from fetchers.test_all.url_scrapers.yp_url_and_phone_scraper import yp_url_and_phone_scraper
from fetchers.test_all.utils.clean_utils import (format_phone_number, remove_phone_format,
                                                 string_cleaner)


def get_locations():

    with open('valid_zipcodes.csv', 'r') as f:
        lines = [line.replace('\n', '') for line in f.readlines()]

    with open('CAN_city.csv', 'r') as f:
        canada_lines = [line.replace('\n', '')[:-1]
                        for line in f.readlines()]

    for line in lines + canada_lines:
        yield line


space = "*" * 75

verticals = ["hvac"]  # 'plumbing', 'restoration'

# , "24715", "01035", "01036", "39823", "61232", "83543", "99841", "85033"
locations = get_locations()

firefox_options = Options()
firefox_options.headless = True
driver = webdriver.Firefox(
    executable_path="/usr/local/share/geckodriver", options=firefox_options)


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


def yellowpages_data_scraper(url, source_phone):
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
    except:
        raw_input("Error on page loading")
    try:
        body = page_soup.find("body").text.strip()
        if "Forbidden" in body:
            raw_input("Forbidden, Please change IP an press Enter")
    except:
        pass
    try:
        company_name = page_soup.find("div", {"class": "sales-info"})
        company_name = company_name.text.strip()
        company_name = string_cleaner(company_name)
        if 'add to favorites' in company_name:
            company_name = company_name.split('add to favorites')[0]
        print("Company Name: " + company_name)
    except:
        company_name = ""
    try:
        phone_number = page_soup.find("p", {"class": "phone"})
        phone_number = phone_number.text.strip()
        phone_number = remove_phone_format(phone_number)
        if phone_number == source_phone:
            validated = True
        print("Phone Number: " + phone_number)
    except:
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
    except:
        rating = ""
    try:
        street_address = str(page_soup.find(
            "script", {"type": "application/ld+json"}))
        street_address = street_address.split('streetAddress":"')[1]
        street_address = street_address.split('"')[0]
        street_address = string_cleaner(street_address)
        print("Street Address: " + street_address)
    except:
        street_address = ""
    try:
        city = str(page_soup.find("script", {"type": "application/ld+json"}))
        city = city.split('addressLocality":"')[1]
        city = city.split('"')[0]
        city = string_cleaner(city)
        print("City: " + city)
    except:
        city = ""
    try:
        state = str(page_soup.find("script", {"type": "application/ld+json"}))
        state = state.split('addressRegion":"')[1]
        state = state.split('"')[0]
        state = string_cleaner(state)
        print("State: " + state)
    except:
        state = ""
    try:
        zip_code = str(page_soup.find(
            "script", {"type": "application/ld+json"}))
        zip_code = zip_code.split('postalCode":"')[1]
        zip_code = zip_code.split('"')[0]
        zip_code = string_cleaner(zip_code)
        print("Zip Code: " + zip_code)
    except:
        zip_code = ""
    try:
        email_address = page_soup.find(
            "div", {"class": "business-card-footer"})
        email_address = str(email_address)
        email_address = email_address.split('mailto:')[1]
        email_address = email_address.split('"')[0]
        email_address = string_cleaner(email_address)
        print("Email: " + email_address)
    except:
        email_address = ""
    try:
        years_container = page_soup.find("div", {"class": "number"})
        years = years_container.text.strip()
        years = string_cleaner(years)
        print("Years in business " + years)
    except:
        years = ""
    try:
        reviews = str(page_soup.find(
            "script", {"type": "application/ld+json"}))
        reviews = reviews.split('reviewCount":')[1]
        reviews = reviews.split('}')[0]
        reviews = string_cleaner(reviews)
        print("Reviews: " + reviews)
    except:
        reviews = ""
    try:
        website = str(page_soup.find(
            "script", {"type": "application/ld+json"}))
        website = website.split('"&nbsp;http://')[1]
        website = website.split('&nbs')[0]
        website = string_cleaner(website)
        print("Website " + website)
    except:
        website = ""
    try:
        temp_phone_list = []
        extra_phone_container = page_soup.find("dd", {"class": "extra-phones"})
        extra_phone_container = extra_phone_container.findAll("span")
    except:
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
        except:
            alt_phone_2 = ""
        if alt_phone_2 == source_phone:
            validated = True
        print("Alt Phone Number 1: " + alt_phone_1 +
              '\n' + "Alt Phone Number 2: " + alt_phone_2)
    try:
        category_container = page_soup.find("dd", {"class": "categories"})
        category_container = category_container.text.strip()
        category_container = category_container.split(',')
    except:
        category_1 = ""
        category_2 = ""
    else:
        try:
            category_1 = category_container[0]
            category_1 = string_cleaner(category_1)
            print("Category 1: " + category_1)
        except:
            category_1 = ""
        try:
            category_2 = category_container[1]
            category_2 = string_cleaner(category_2)
            print("Category 2: " + category_2)
        except:
            category_2 = ""
    try:
        accepted_payment = page_soup.find(
            "dd", {"class": "payment"}).text.strip()
        accepted_payment = string_cleaner(accepted_payment)
        print("Accepted Payment: " + accepted_payment)
    except:
        accepted_payment = ""
    try:
        aka = page_soup.find("dd", {"class": "aka"}).text.strip()
        aka = string_cleaner(aka)
        print("Alias: " + aka)
    except:
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
    except:
        alt_email = ""
    print("Validated: " + str(validated))
    try:
        new_data_list.append(company_name)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(phone_number)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(rating)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(street_address)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(city)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(state)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(zip_code)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(email_address)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(years)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(reviews)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(website)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(alt_phone_1)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(alt_phone_2)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(category_1)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(category_2)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(accepted_payment)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(aka)
    except:
        new_data_list.append("error")
    try:
        new_data_list.append(alt_email)
    except:
        new_data_list.append("error")
    new_data_list.append(validated)
    return new_data_list


def primary_sources_merge(dict_one, dict_two, dict_three, number_of_empty_lists):
    de_duped_lead_list = []
    unique_phone_list = []
    all_results = dict_one + dict_two + dict_three
    all_results = [elem for elem in all_results if elem]

    for result in all_results:
        phone_number = result.get("phone")
        if phone_number in unique_phone_list:
            pass
        else:
            unique_phone_list.append(phone_number)
    print(all_results)
    for phone in unique_phone_list:
        unique_lead = {}
        for result in all_results:
            if phone == result.get("phone"):
                url_key = list(result.keys())[1]
                unique_lead["phone"] = phone
                unique_lead[url_key] = list(result.values())[1]
        de_duped_lead_list.append(unique_lead)
    return de_duped_lead_list


def valid_domain_check(url):
    valid_domain = False
    valid_domains = ['yelp.com', 'bbb.org', 'yellowpages.com',
                     'manta.com', 'mapquest.com', 'chamberofcommerce.com']
    for domain in valid_domains:
        if domain in url:
            valid_domain = True
            break
    return valid_domain


def source_url_filter(url):
    valid_url = False
    if 'yelp.com' in url:
        if '/biz/' in url:
            valid_url = True
    elif 'bbb.org' in url:
        if '/profile/' in url:
            valid_url = True
    elif 'yellowpages.com' in url:
        if '/mip/' in url:
            valid_url = True
    elif 'mapquest.com' in url:
        if '/us/' in url:
            valid_url = True
        if '/ca/' in url:
            valid_url = True
        if '/canada/' in url:
            valid_url = True
    elif 'manta.com' in url:
        if '/c/' in url:
            valid_url = True
    elif 'chamberofcommerce.com' in url:
        if '/united-states/' in url:
            valid_url = True
        if '/canada/' in url:
            valid_url = True
    return valid_url


def browser_phone_translater(phone_number):
    if isinstance(phone_number, bytes):
        phone_number = phone_number.decode("utf-8")

    translated_phone = phone_number.replace("(", "%28")
    translated_phone = translated_phone.replace(")", "%29")
    translated_phone = translated_phone.replace(" ", "+")
    return translated_phone


def info_scraper(phone_number, pages_per_search_engine):
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
        except:
            pass
        try:
            html_string = (str(page_soup))
            html_string = html_string.split("</head>")[1]
            page_soup = soup(html_string, 'html.parser')
            blocked_check = page_soup.find("div", {"class": "error-code"})
            blocked_check = blocked_check.text.strip()
        except:
            pass
        try:
            if 'ERR_EMPTY' in blocked_check:
                blocked = True
        except:
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
    return info_results, blocked


def ask_scraper(phone_number, pages_per_search_engine):
    # print(space)
    ask_results = []
    pages_per_search_engine = pages_per_search_engine + 1
    for i in range(1, pages_per_search_engine):
        translated_phone = browser_phone_translater(phone_number)
        search_url = 'https://www.ask.com/web?o=0&l=dir&qo=homepageSearchBox&q=' + \
            translated_phone + '&page=' + str(i)
        driver.get(search_url)
        html_page = driver.page_source
        page_soup = soup(html_page, 'html.parser')
        try:
            no_result_container = page_soup.find(
                "div", {"class": "PartialSearchResults-noresults-body"})
            no_result_container = no_result_container.text.strip()
            if 'we did not find any results' in no_result_container:
                break
        except:
            pass
        result_containers = page_soup.findAll(
            "div", {"class": "PartialSearchResults-item"})
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
                            if link in ask_results:
                                pass
                            else:
                                ask_results.append(link)
                                # print("ask ---> " + link)
    return ask_results


def google_scraper(phone_number, pages_per_search_engine):
    blocked = False
    google_results = []
    # pages_per_search_engine = pages_per_search_engine + 1
    pages_per_search_engine = pages_per_search_engine*10
    translated_phone = browser_phone_translater(phone_number)
    search_url = 'https://www.google.com/search?q=' + \
        translated_phone + '&num=' + str(pages_per_search_engine)
    driver.get(search_url)
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


def bing_scraper(phone_number, pages_per_search_engine):
    # print(space)
    bing_results = []
    # pages_per_search_engine = pages_per_search_engine + 1
    pages_per_search_engine = pages_per_search_engine*10
    translated_phone = browser_phone_translater(phone_number)
    search_url = 'https://www.bing.com/search?q=' + \
        translated_phone + '&count=' + str(pages_per_search_engine)
    driver.get(search_url)
    html_page = driver.page_source
    page_soup = soup(html_page, 'html.parser')
    result_containers = page_soup.findAll("li", {"class": "b_algo"})
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
                        if link in bing_results:
                            pass
                        else:
                            bing_results.append(link)
                            # print("bing ---> " + link)
    return bing_results


def append_source_urls_to_lead(lead, unique_url_list):
    for url in unique_url_list:
        if 'yelp.com' in url:
            try:
                if lead["yelp url"]:
                    pass
            except KeyError:
                lead["yelp url"] = url
        if 'bbb.org' in url:
            try:
                if lead["bbb url"]:
                    pass
            except KeyError:
                lead["bbb url"] = url
        if 'yellowpages.com' in url:
            try:
                if lead["yp url"]:
                    pass
            except KeyError:
                lead["yp url"] = url
        if 'mapquest.com' in url:
            try:
                if lead["mapquest url"]:
                    pass
            except KeyError:
                lead["mapquest url"] = url
        if 'manta.com' in url:
            try:
                if lead["manta url"]:
                    pass
            except KeyError:
                lead["manta url"] = url
        if 'chamberofcomomerce.com' in url:
            try:
                if lead["chamberofcomomerce url"]:
                    pass
            except KeyError:
                lead["chamberofcomomerce url"] = url
    return lead


def search_engine_scraper(unique_list, pages_per_search_engine):
    blocked_search_engine_count = 0
    list_of_enhanced_leads = []
    for lead in unique_list:
        unique_url_list = []
        phone_number = lead['phone']
        formatted_phone = format_phone_number(phone_number)
        info_url_list, info_blocked = info_scraper(
            formatted_phone, pages_per_search_engine)
        ask_url_list = ask_scraper(formatted_phone, pages_per_search_engine)
        google_url_list, google_blocked = google_scraper(
            formatted_phone, pages_per_search_engine)
        bing_url_list = bing_scraper(formatted_phone, pages_per_search_engine)
        found_urls = info_url_list + ask_url_list + google_url_list + bing_url_list
        for i in found_urls:
            for v in lead.values():
                if i == v:
                    pass
                else:
                    if i in unique_url_list:
                        pass
                    else:
                        unique_url_list.append(i)
        enhanced_lead = append_source_urls_to_lead(lead, unique_url_list)
        list_of_enhanced_leads.append(enhanced_lead)
        block_check_list = []
        block_check_list.append(info_blocked)
        block_check_list.append(google_blocked)
        # block_check_list.append(ask_blocked)
        # block_check_list.append(bing_blocked)
        blocked_search_engine_count = 0
        for i in block_check_list:
            if i:
                blocked_search_engine_count = blocked_search_engine_count + 1
        if blocked_search_engine_count >= 3:
            pass  # Add Get unlockied function here to automatically chanfe IP address
    return list_of_enhanced_leads


def check_for_no_results(dict_one, dict_two, dict_three):
    empty_list_count = 0
    if dict_one[0] == {}:
        empty_list_count = empty_list_count + 1
    if dict_two == []:
        empty_list_count = empty_list_count + 1
    if dict_three == []:
        empty_list_count = empty_list_count + 1
    return empty_list_count


def post_enhancement_data_scrape(enhanced_lead_data):
    for enhanced_lead in enhanced_lead_data:
        new_data_dictionaries = []
        phone_number = enhanced_lead["phone"]
        for value in enhanced_lead.values():
            if 'yelp.com' in value:
                already_scraped = False
                for row in new_yelp_leads:
                    yelp_url = row['yelp url']
                    if value == yelp_url:
                        already_scraped = True
                        break
                if already_scraped:
                    pass
                else:
                    # temp_list = [value]
                    yelp_data = yelp_data_scraper(driver, value, phone_number)
                    new_yelp_data = yelp_data[0]
                    new_data_dictionaries.append(new_yelp_data)
            if 'bbb.org' in value:
                already_scraped = False
                for row in new_bbb_url_and_phones:
                    bbb_url = row["bbb url"]
                    if value == bbb_url:
                        already_scraped = True
                        break
                if already_scraped:
                    pass
                else:
                    new_bbb_data = bbb_data_scraper(value, phone_number)
            if 'yellowpages.com' in value:
                already_scraped = False
                for row in new_yp_url_and_phones:
                    try:
                        yp_url = row[0]
                    except:
                        yp_url = row["yp url"]
                    if value == yp_url:
                        already_scraped = True
                        break
                if already_scraped:
                    print("already_scraped")
                else:
                    new_yp_data = yellowpages_data_scraper(value, phone_number)
            if 'manta.com' in value:
                new_manta_data = manta_data_scraper(value, phone_number)
            if 'mapquest.com' in value:
                new_mapquest_data = mapquest_data_scraper(value, phone_number)
            if 'chamberofcommerce.com' in value:
                new_chamberofcommerce_data = chamberofcommerce_data_scraper(
                    value, phone_number)


def get_verticals_and_location_crawled():
    filenames = os.listdir("data/enhanced")
    print("files", filenames)

    locations_and_verticals = set(
        [tuple(filename.split('/')[-1].split('-')[:2]) for filename in filenames])
    return locations_and_verticals


limit = 0
verticals_and_locations_crawled = get_verticals_and_location_crawled()
print(verticals_and_locations_crawled)

s = time.perf_counter()

try:
    for vertical in verticals:
        for location in locations:
            if (vertical, location) in verticals_and_locations_crawled:
                continue
            if limit >= 200:
                break
            limit += 1
            vertical_and_location_name = vertical + '-' + location
            file_name = vertical + '-' + location + '-phone_and_url_scrape.xlsx'
            print(space + "\n" "Current vertical: " + vertical +
                  "\n" + "Current location: " + location + "\n" + space)
            print("[*] Scraping for yelp urls [*]")
            unique_yelp_url_list = yelp_url_scraper(driver, vertical, location)
            print("[*] Scraping data from yelp urls [*]")
            new_yelp_leads = yelp_data_scraper(
                driver, unique_yelp_url_list, '')
            print("[*] Saving scraped yelp data [*]")
            dictionary_dataframe = pd.DataFrame(new_yelp_leads)
            dictionary_dataframe.to_excel(
                "data/yelp_data/" + vertical + "-" + location + "-yelp_data.xlsx")
            print("Saved")
            print("[*] Extracting phones and urls from yelp data [*]")
            new_yelp_url_and_phones = []
            if new_yelp_leads == []:
                new_yelp_url_and_phones.append({})
            else:
                for lead in new_yelp_leads:
                    yelp_url_and_phone_dict = {}
                    phone_number = lead["phone"]
                    source_url = lead["yelp url"]
                    yelp_url_and_phone_dict["phone"] = phone_number
                    yelp_url_and_phone_dict["yelp url"] = source_url
                    new_yelp_url_and_phones.append(yelp_url_and_phone_dict)
            print("[*] Scraping for bbb Phones and urls [*]")
            new_bbb_url_and_phones = bbb_url_and_phone_scraper(
                driver, vertical, location)
            print("[*] Scraping for yp phones and urls [*]")
            new_yp_url_and_phones = yp_url_and_phone_scraper(
                vertical, location)
            print("[*] Checking for empty lists [*]")
            number_of_empty_lists = check_for_no_results(
                new_yelp_url_and_phones, new_bbb_url_and_phones, new_yp_url_and_phones)
            if number_of_empty_lists == 3:
                print("[*] No new data found for " +
                      vertical_and_location_name + " [*]")
            else:
                print("[*] Merging yelp, bbb and yp phones and urls [*]")
                de_duped_lead_list = primary_sources_merge(
                    new_yelp_url_and_phones, new_bbb_url_and_phones, new_yp_url_and_phones, number_of_empty_lists)
                print("[*] Saving yelp, bbb and yp source phones and urls [*]")
                dictionary_dataframe = pd.DataFrame(de_duped_lead_list)
                dictionary_dataframe.to_excel(
                    "data/phones_urls/" + vertical + "-" + location + "-phones_and_urls.xlsx")
                print("Saved")
                print("[*] Passing list of scraped phone numbers through the search engine scraper [*]\n[*] Adding enhancmenet source urls to phone numbers [*]")
                enhanced_lead_data = search_engine_scraper(
                    de_duped_lead_list, 2)
                print("[*] Saving enhanced phones and urls [*]")
                dictionary_dataframe = pd.DataFrame(enhanced_lead_data)
                dictionary_dataframe.to_excel(
                    "data/enhanced/" + vertical + "-" + location + "-phones_and_urls_enhanced.xlsx")
                print("Saved")
            # post_enhancement_data_scrape(enhanced_lead_data)
finally:
    driver.close()
e = time.perf_counter()
print(f"Finished in {e-s}")
