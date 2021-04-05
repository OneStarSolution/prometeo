import os
import time

import argparse
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from selenium.webdriver.firefox.options import Options

from fetchers.test_all.utils.clean_utils import format_phone_number
from fetchers.test_all.data_scrapers.yelp_data_scraper import yelp_data_scraper
# from fetchers.test_all.data_scrapers.bbb_data_scraper import bbb_data_scraper
from fetchers.test_all.url_scrapers.yelp_url_scraper import yelp_url_scraper
from fetchers.test_all.url_scrapers.yelp import yelp_url_scraper_test
from fetchers.test_all.url_scrapers.bbb_url_and_phone_scraper import bbb_url_and_phone_scraper
from fetchers.test_all.url_scrapers.yp_url_and_phone_scraper import yp_url_and_phone_scraper
from fetchers.test_all.search_engines.ask_scraper import ask_scraper
from fetchers.test_all.search_engines.bing_scraper import bing_scraper
from fetchers.test_all.search_engines.info_scraper import info_scraper
from fetchers.test_all.search_engines.google_scraper import google_scraper


def get_locations():

    with open('zipcodes_to_crawl.csv', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    redistribution = []
    # if os.path.isfile('redistribution.txt'):
    #     print("reading redistribution")
    #     with open("redistribution.txt") as f:
    #         redistribution = f.readlines()

    # with open('CAN_city.csv', 'r') as f:
    #     canada_lines = [line.replace('\n', '')[:-1]
    #                     for line in f.readlines()]

    # for line in lines + canada_lines:
    for line in lines:
        yield line.strip().replace('\n', '').replace('$', '')


space = "*" * 75

# 'plumbing', 'restoration'
verticals = ["water treatment"]

locations = get_locations()


def create_driver():
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(
        executable_path="/usr/local/share/geckodriver", options=firefox_options)
    driver.set_page_load_timeout(30)
    return driver


def primary_sources_merge(dict_one, dict_two, dict_three, number_of_empty_lists):
    de_duped_lead_list = []
    unique_phone_list = set()
    all_results = dict_one + dict_two + dict_three
    all_results = [elem for elem in all_results if elem]

    for result in all_results:
        phone_number = result.get("phone")
        if phone_number in unique_phone_list:
            pass
        else:
            unique_phone_list.add(phone_number)

    for phone in unique_phone_list:
        unique_lead = {}
        for result in all_results:
            if phone == result.get("phone"):
                url_key = [key for key in result.keys() if key != "phone"][0]
                unique_lead["phone"] = phone
                unique_lead[url_key] = result.get(url_key)
        de_duped_lead_list.append(unique_lead)

    return de_duped_lead_list


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


def search_engine_scraper(driver, unique_list, pages_per_search_engine):
    blocked_search_engine_count = 0
    list_of_enhanced_leads = []
    for lead in unique_list:
        unique_url_list = []
        phone_number = lead['phone']
        formatted_phone = format_phone_number(phone_number)
        # info_url_list, info_blocked = info_scraper(
        #     driver, formatted_phone, pages_per_search_engine)
        ask_url_list = ask_scraper(
            driver, formatted_phone, pages_per_search_engine)
        google_url_list, google_blocked = google_scraper(
            driver, formatted_phone, pages_per_search_engine)
        bing_url_list = bing_scraper(
            driver, formatted_phone, pages_per_search_engine)
        # found_urls = info_url_list + ask_url_list + google_url_list + bing_url_list
        found_urls = ask_url_list + google_url_list + bing_url_list

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
        # block_check_list.append(info_blocked)
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


# def post_enhancement_data_scrape(enhanced_lead_data):
#     for enhanced_lead in enhanced_lead_data:
#         new_data_dictionaries = []
#         phone_number = enhanced_lead["phone"]
#         for value in enhanced_lead.values():
#             if 'yelp.com' in value:
#                 already_scraped = False
#                 for row in new_yelp_leads:
#                     yelp_url = row['yelp url']
#                     if value == yelp_url:
#                         already_scraped = True
#                         break
#                 if already_scraped:
#                     pass
#                 else:
#                     # temp_list = [value]
#                     yelp_data = yelp_data_scraper(driver, value, phone_number)
#                     new_yelp_data = yelp_data[0]
#                     new_data_dictionaries.append(new_yelp_data)
#             if 'bbb.org' in value:
#                 already_scraped = False
#                 for row in new_bbb_url_and_phones:
#                     bbb_url = row["bbb url"]
#                     if value == bbb_url:
#                         already_scraped = True
#                         break
#                 if already_scraped:
#                     pass
#                 else:
#                     new_bbb_data = bbb_data_scraper(driver, value, phone_number)
#             if 'yellowpages.com' in value:
#                 already_scraped = False
#                 for row in new_yp_url_and_phones:
#                     try:
#                         yp_url = row[0]
#                     except:
#                         yp_url = row["yp url"]
#                     if value == yp_url:
#                         already_scraped = True
#                         break
#                 if already_scraped:
#                     print("already_scraped")
#                 else:
#                     new_yp_data = yellowpages_data_scraper(driver, value, phone_number)
#             if 'manta.com' in value:
#                 new_manta_data = manta_data_scraper(value, phone_number)
#             if 'mapquest.com' in value:
#                 new_mapquest_data = mapquest_data_scraper(value, phone_number)
#             if 'chamberofcommerce.com' in value:
#                 new_chamberofcommerce_data = chamberofcommerce_data_scraper(
#                     value, phone_number)


def get_verticals_and_location_crawled():
    filenames = os.listdir("data/enhanced")

    locations_and_verticals = set(
        [tuple(filename.split('/')[-1].split('-')[:2]) for filename in filenames])
    return locations_and_verticals


def run(vertical, location):
    driver = create_driver()
    try:
        location = location.zfill(5) if location.isnumeric() else location
        vertical_and_location_name = vertical + '-' + location

        print(space + "\n" "Current vertical: " + vertical +
              "\n" + "Current location: " + location + "\n" + space)
        # print("[*] Scraping for yelp urls [*]")

        # unique_yelp_url_list = yelp_url_scraper_test(
        #     driver, vertical, location)

        # print("[*] Scraping data from yelp urls [*]")
        # new_yelp_leads = []

        # new_yelp_leads = yelp_data_scraper(
        #     driver, unique_yelp_url_list, '')

        # print("[*] Saving scraped yelp data [*]")
        # dictionary_dataframe = pd.DataFrame(new_yelp_leads)
        # dictionary_dataframe.to_excel(
        #     "data/yelp_data/" + vertical + "-" + location + "-yelp_data.xlsx")
        # print("Saved")
        # print("[*] Extracting phones and urls from yelp data [*]")
        # new_yelp_url_and_phones = []
        # if new_yelp_leads == []:
        #     new_yelp_url_and_phones.append({})
        # else:
        #     for lead in new_yelp_leads:
        #         yelp_url_and_phone_dict = {}
        #         phone_number = lead["phone"]
        #         source_url = lead["yelp url"]
        #         yelp_url_and_phone_dict["phone"] = phone_number
        #         yelp_url_and_phone_dict["yelp url"] = source_url
        #         new_yelp_url_and_phones.append(yelp_url_and_phone_dict)

        print("[*] Scraping for bbb Phones and urls [*]")
        new_bbb_url_and_phones = bbb_url_and_phone_scraper(
            driver, vertical, location)
        print("[*] Scraping for yp phones and urls [*]")
        new_yp_url_and_phones = yp_url_and_phone_scraper(
            driver, vertical, location)
        print("[*] Checking for empty lists [*]")
        # comment when you want to run yelp
        new_yelp_url_and_phones = [{}]
        number_of_empty_lists = check_for_no_results(
            new_yelp_url_and_phones, new_bbb_url_and_phones, new_yp_url_and_phones)
        if number_of_empty_lists == 3:
            print("[*] No new data found for " +
                  vertical_and_location_name + " [*]")
        else:
            print("[*] Merging yelp, bbb and yp phones and urls [*]")
            de_duped_lead_list = primary_sources_merge(
                new_yelp_url_and_phones, new_bbb_url_and_phones, new_yp_url_and_phones,
                number_of_empty_lists)
            print("[*] Saving yelp, bbb and yp source phones and urls [*]")
            dictionary_dataframe = pd.DataFrame(de_duped_lead_list)
            dictionary_dataframe.to_excel(
                "data/phones_urls/" + vertical.replace(" ", "_") + "-" + location + "-phones_and_urls.xlsx")
            print("Saved")
            print(
                "[*] Passing list of scraped phone numbers through the search engines [*]")
            print("[*] Adding enhancmenet source urls to phone numbers [*]")
            enhanced_lead_data = search_engine_scraper(
                driver, de_duped_lead_list, 2)
            print("[*] Saving enhanced phones and urls [*]")
            dictionary_dataframe = pd.DataFrame(enhanced_lead_data)
            dictionary_dataframe.to_excel(
                "data/enhanced/" + vertical.replace(" ", "_") + "-" + location + "-phones_and_urls_enhanced.xlsx")
            print("Saved")
        # post_enhancement_data_scrape(enhanced_lead_data)
    except Exception as e:
        print(e)
    finally:
        driver.close()


def main():
    # Parse commands
    parser = argparse.ArgumentParser(description='Process crawl params.')
    parser.add_argument('--workers', metavar='workers', type=int, dest="workers",
                        default=1, help='number of workers', required=False)
    args = parser.parse_args()

    print(f"\nRunning with {args.workers} workers\n")

    limit = 0
    verticals_and_locations_crawled = get_verticals_and_location_crawled()
    print(verticals_and_locations_crawled)

    s = time.perf_counter()

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        for vertical in verticals:
            for location in locations:
                if (vertical.replace(" ", "_"), location) in verticals_and_locations_crawled:
                    continue
                if limit >= 5000:
                    break
                limit += 1
                executor.submit(run, vertical, location)

    e = time.perf_counter()

    print(f"Finished in {e-s}")


if __name__ == "__main__":
    main()
