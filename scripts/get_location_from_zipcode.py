import requests
from bs4 import BeautifulSoup


def get_html(zipcode):
    target_url = f'https://www.unitedstateszipcodes.org/{zipcode}/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
        "referer": target_url,
    }
    res = requests.get(target_url, headers=headers)

    if res.status_code != 200:
        print(f"Error in the request {res.status_code}")
        return ""
    return res.text


def parse_location(soup):
    map_info_container = soup.find('div', {"id": "map-info"})
    rows = map_info_container.find_all('tr')

    location = {}

    for row in rows:
        key = row.find('th')
        value = row.find('td')

        if not key or not value:
            continue

        key = key.text.strip().replace(':', '').lower()
        value = value.text.strip().lower()

        if "post" in key:
            city, state = value.split("(")[0].split(",")
            city, state = city.strip(), state.strip()
            location["city"] = city
            location["state"] = state
            continue

        location[key] = value

    return location


def get_location(zipcode):
    html = get_html(zipcode)
    soup = BeautifulSoup(html, features="lxml")

    location = parse_location(soup)
    return location
