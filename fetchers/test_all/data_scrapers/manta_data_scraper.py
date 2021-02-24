import time
import re

from datetime import datetime
from bs4 import BeautifulSoup


class MantaDataScrape:
    CLASSES = {
        "ask_captcha_container": "cf-subheadline",
        "location_list": "text-gray-dark",
    }

    IDS = {
        "name_container": "alertContainer",
        "contact_container": "contactContent",
        "datails_container": "detailsContent",
        "reviews_container": "reviewsContent",
    }

    def __init__(self, html: str = None):
        if not html:
            with open("manta.html", "r") as f:
                html = f.read()

        self.soup = BeautifulSoup(html, features="html.parser")
        self.summary = {}

    def verify(self):
        ask_captcha_container = self.soup.find(
            "h2", {"class": self.CLASSES.get("ask_captcha_container")})
        ask_captcha_text = "please complete the security check to access"

        if ask_captcha_container and ask_captcha_text in ask_captcha_container:
            print("Ask for captcha")
            return False

        containers_found = []
        for container_id in self.IDS:
            container = self.soup.find(
                "div", {"id": self.IDS.get(container_id)})
            containers_found.append(container)

        return all(containers_found)

    def parse(self):
        self.summary["name"] = self.get_name()
        self.summary["claimed"] = self.is_claim()
        self.summary["location"] = self.get_location()
        self.summary["phone"] = self.get_phone()
        self.summary["website"] = self.get_website()
        self.summary["years"] = self.get_years_from_established()
        self.summary["employees"] = self.get_employees()
        self.summary["contacts"] = self.get_contacts()
        self.summary["reviews"] = self.get_reviews()

    def get_name(self) -> str:
        return self.soup.find("div", {
            "id": self.IDS.get("name_container")}).find("div").text.strip()

    def is_claim(self) -> bool:
        return True if "claimed" in self.soup.find("div", {
            "id": self.IDS.get("name_container")}).text.strip().lower() else False

    def get_location(self) -> dict:
        location = {}
        location_list = self.soup.find("div", {
            "id": self.IDS.get("contact_container")}).find('ul', {
                "class": self.CLASSES.get("location_list")}).find_all("li")

        if not location_list or len(location_list) != 3:
            print("Location list is different from what we")
            return location

        city, state, zipcode = location_list[2].text.strip().replace(
            ",", "").split()

        location = {
            "street": location_list[1].text,
            'state': state,
            'zipcode': zipcode,
            "city": city,
        }

        return location

    def get_phone(self):
        return self.soup.find("a", {"href": re.compile("^tel")})["href"].replace("tel:", "")

    # NOTE: THIS COULD SHOULD BE OPMTIMIZED BEFORE PRODUCTION
    def get_website(self):
        links = self.soup.find("div", {
            "id": self.IDS.get("contact_container")}).find_all("a")
        i = [a.find("i") for a in links]

        i = [elem for elem in i if elem and "Visit" in elem.next_sibling.strip()]

        href = ""
        if i:
            href = i[0].parent["href"]
            href = re.search(r"(www.*)", href).group(1).split("&")[0]

        return href

    def get_years_from_established(self):
        established = int(self.soup.find("div", {
            "id": self.IDS.get("datails_container")}).find(
                "span", string="Year Established").next_sibling.text)
        return datetime.now().year - established

    def get_employees(self):
        str_range = self.soup.find("div", {
            "id": self.IDS.get("datails_container")}).find(
                "span", string="Employees").next_sibling.text

        int_range = list(map(int, str_range.split(" to ")))
        # Aprox of Employees
        return int_range[0] + (int_range[1] - int_range[0]) // 2

    def get_contacts(self) -> dict:
        contacts = {}
        detail_container = self.soup.find("div", {
            "id": self.IDS.get("datails_container")})

        contacts_label = detail_container.find(
            "span", string="Contacts").next_sibling.text

        if "show" not in contacts_label.lower():
            return contacts

        hidden_uls = detail_container.find("ul", {"class": "hidden"})

        for ul in hidden_uls.find_all("ul"):
            for li in ul.find_all("li"):
                spans = li.find_all("span")
                key = spans[0].text.strip().lower()
                value = spans[1].text.strip()

                if key and value:
                    contacts[key] = value

        return contacts

    def get_reviews(self):
        return int(re.search(r"\((.*)\)", self.soup.find("div", {
            "id": self.IDS.get("reviews_container")}).text).group(1))


# _max = 0
# _min = 1000
# _sum = 0
# n = 100
# m = MantaDataScrape()
# for i in range(n):
#     s = time.perf_counter()
#     m.parse()
#     e = time.perf_counter()
#     res = e-s
#     _max = max(res, _max)
#     _min = min(res, _min)
#     _sum += res
# print(f"Max: {_max} Min: {_min} Avg: {_sum/n}")
