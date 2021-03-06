import re
import json

from bs4 import BeautifulSoup as soup

from fetchers.test_all.utils.duplicate_checker import duplicate_checker
from fetchers.test_all.utils.clean_utils import string_cleaner


def yelp_data_scraper(driver, url_list, source_phone=""):

    string = False
    accepts_cc = ""
    phone_number = ""
    category_two = ""
    category_three = ""
    category_three = ""
    contact_name = ""
    contact_title = ""
    website = ""
    if isinstance(url_list, str):
        validated = False
        single_value = url_list
        string = True
        url_list = [url_list]

    new_lead_dict_list = []
    for url in url_list:

        # print(space)
        temp_snippet_list = []
        try:
            driver.get("https://" + url)
            # time.sleep(1.5)
            html_page = driver.page_source
            page_soup = soup(html_page, 'html.parser')
        except Exception as e:
            print("Error fetching the html for this page:" + url)
            print(e)
            continue

        # Verify
        if "not allowed to access this page" in page_soup.text.lower():
            print("exceeded request limit, change ip address to continue")
            break

        json_snippets = page_soup.findAll(
            "script", {"type": "application/ld+json"})

        json_block_one = {}

        if len(json_snippets) == 1:
            snippet = json_snippets[0]
            snippet = str(snippet).split(
                '<script type="application/ld+json">')[1]
            snippet = snippet.split('</script>')[0]
            json_block_one = json.loads(snippet)
            try:
                phone_number = str(json_block_one.get("telephone"))
                phone_number = str(json_block_one.get("telephone"))
                phone_number = re.sub("[^0-9]", "", phone_number)
                phone_number = string_cleaner(phone_number)
                print("Phone number: " + phone_number)
            except Exception as e:
                phone_number = " "
        else:
            for snippet in json_snippets:
                clean_snippet_list = []
                snippet = str(snippet).split(
                    '<script type="application/ld+json">')[1]
                snippet = snippet.split('</script>')[0]
                temp_snippet_list.append(snippet)
            try:
                json_block_one = json.loads(temp_snippet_list[0])
            except Exception as e:
                print(e)
                pass
            else:
                try:
                    phone_number = str(json_block_one.get("telephone"))
                    phone_number = re.sub("[^0-9]", "", phone_number)
                    phone_number = string_cleaner(phone_number)
                    print("Phone number: " + phone_number)
                except Exception as e:
                    phone_number = " "

        status = True if string else duplicate_checker('phone', phone_number)
        if status:
            new_lead_dict = {}
            new_lead_dict["yelp url"] = url
            validated = ""
            if phone_number == source_phone:
                validated = True
            if source_phone == "":
                validated = "null"

            new_lead_dict["validated"] = validated
            new_lead_dict["phone"] = phone_number
            try:
                company_name = str(json_block_one.get("name"))
                company_name = string_cleaner(company_name)

            except Exception as e:
                company_name = ""
            new_lead_dict["company_name"] = company_name
            try:
                address = json_block_one.get(
                    "address", {}).get("streetAddress")
                address = string_cleaner(address)

            except Exception as e:
                address = ""
            new_lead_dict["address"] = address
            try:
                city = str(json_block_one.get(
                    "address", {}).get("addressLocality"))
                city = string_cleaner(city)

            except Exception as e:
                city = ""
            new_lead_dict["city"] = city
            try:
                state = str(json_block_one.get(
                    "address", {}).get("addressRegion"))
                state = string_cleaner(state)

            except Exception as e:
                state = ""
            new_lead_dict["state"] = state
            try:
                zip_code = json_block_one.get("address", {}).get("postalCode")
                zip_code = string_cleaner(zip_code)

            except Exception as e:
                zip_code = ""
            new_lead_dict["zip_code"] = zip_code
            try:
                rating = str(json_block_one.get(
                    "aggregateRating", {}).get("ratingValue"))
                rating = string_cleaner(rating)

            except Exception as e:
                rating = ""
            new_lead_dict["rating"] = rating
            try:
                review = str(json_block_one.get(
                    "aggregateRating", {}).get("reviewCount"))
                review = string_cleaner(review)

            except Exception as e:
                review = ""
            new_lead_dict["review"] = review
            back_up_cat_containers = []
            try:
                category_container = page_soup.findAll(
                    "div", {"class": "arrange__373c0__2C9bH gutter-2__373c0__1DiLQ border-color--default__373c0__3-ifU"})
                category_container = category_container[1]
                categories = category_container.findAll(
                    "span", {"class": "text__373c0__2Kxyz text-color--black-regular__373c0__2vGEn text-align--left__373c0__2XGa- text-weight--semibold__373c0__2l0fe text-size--large__373c0__3t60B"})
                try:
                    back_up_cat_containers = category_container.findAll(
                        "span", {"class": "display--inline__373c0__3JqBP margin-r1__373c0__zyKmV border-color--default__373c0__3-ifU"})
                except Exception as e:
                    pass
            except Exception as e:
                category_one = ""
                category_two = ""
                category_three = ""
            else:
                try:
                    category_one = categories[0].text.strip()
                except Exception as e:
                    category_one = back_up_cat_containers[0].text.strip()
                    if 'review' in category_one:
                        category_one = back_up_cat_containers[1].text.strip()
                        try:
                            category_two = back_up_cat_containers[2].text.strip(
                            )
                            try:
                                category_three = back_up_cat_containers[3].text.strip(
                                )
                            except Exception as e:
                                category_three = ""
                        except Exception as e:
                            category_two = ""
                            category_three = ""
                    else:
                        try:
                            category_two = back_up_cat_containers[1].text.strip(
                            )
                            try:
                                category_three = back_up_cat_containers[2].text.strip(
                                )
                            except Exception as e:
                                category_three = ""
                        except Exception as e:
                            category_two = ""
                            category_three = ""
                else:
                    try:
                        if 'review' in category_one:
                            category_one = categories[1].text.strip()
                            try:
                                category_two = categories[2].text.strip()
                                try:
                                    category_three = categories[3].text.strip()
                                except Exception as e:
                                    category_three = ""
                            except Exception as e:
                                category_two = ""
                                category_three = ""
                        else:
                            try:
                                category_two = categories[1].text.strip()
                                try:
                                    category_three = categories[2].text.strip()
                                except Exception as e:
                                    category_three = ""
                            except Exception as e:
                                category_two = ""
                                category_three = ""
                    except Exception as e:
                        category_one = ""
                        category_two = ""
                        category_three = ""
            if 'laimed' in category_one:
                category_one = ""
            category_one = string_cleaner(category_one)
            category_two = string_cleaner(category_two)
            category_three = string_cleaner(category_three)
            new_lead_dict["category_one"] = category_one
            new_lead_dict["category_two"] = category_two
            new_lead_dict["category_three"] = category_three

            try:
                website_container = page_soup.findAll(
                    "div", {"class": "arrange__373c0__2C9bH gutter-2__373c0__1DiLQ vertical-align-middle__373c0__1SDTo border-color--default__373c0__3-ifU"})
                for container in website_container:
                    if "Business website" in str(container):
                        website = container.find("a", {"role": "link"})
                        website = website.text.strip()
                        website = string_cleaner(website)

                        break
                    else:
                        website = ""
            except Exception as e:
                website = ""
            new_lead_dict["website"] = website
            try:
                claimed_container = page_soup.find("span", {
                                                   "class": "text__373c0__2Kxyz claim-text--dark__373c0__xRoSM text-color--blue-regular__373c0__QFzix text-align--left__373c0__2XGa- text-weight--semibold__373c0__2l0fe text-bullet--after__373c0__3fS1Z text-size--large__373c0__3t60B"})
                if not claimed_container:
                    claimed_container = page_soup.find("span", {
                                                       "class": "text__373c0__2Kxyz claim-text--dark__373c0__xRoSM text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa- text-weight--semibold__373c0__2l0fe text-bullet--after__373c0__3fS1Z text-size--large__373c0__3t60B"})
                    claimed = claimed_container.text.strip()
                    claimed = string_cleaner(claimed)
                else:
                    claimed = claimed_container.text.strip()
                    claimed = string_cleaner(claimed)
            except Exception as e:
                claimed = ""
            new_lead_dict["claimed"] = claimed
            try:
                about_the_business_container = page_soup.find(
                    "section", {"aria-label": "About the Business"})
                contact_name = about_the_business_container.find(
                    "p", {"class": "text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--large__373c0__3t60B"})
                contact_name = contact_name.text.strip()
                try:
                    contact_title = about_the_business_container.find(
                        "p", {"class": "text__373c0__2Kxyz text-color--black-extra-light__373c0__2OyzO text-align--left__373c0__2XGa-"})
                    contact_title = contact_title.text.strip()
                except Exception as e:
                    contact_title = ""
            except Exception as e:
                contact_name = ""
                contact_title = ""
            contact_name = string_cleaner(contact_name)
            contact_title = string_cleaner(contact_title)
            new_lead_dict["contact_name"] = contact_name
            new_lead_dict["contact_title"] = contact_title

            try:
                question_containers = page_soup.findAll(
                    "div", {"class": "padding-b4__373c0__uiolV border-color--default__373c0__3-ifU"})
                for container in question_containers:
                    container = container.text.strip()
                    if "What forms of payment are accepted" in container:
                        accepts_cc = container.split("?")[1]
                        accepts_cc = string_cleaner(accepts_cc)
                        break
                    else:
                        accepts_cc = ""
            except Exception as e:
                accepts_cc = ""
            new_lead_dict["accepts_cc"] = accepts_cc
            try:
                new_lead_dict_list.append(new_lead_dict)
            except Exception as e:
                pass
    return new_lead_dict_list
