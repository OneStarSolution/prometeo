from bs4 import BeautifulSoup
from datetime import datetime
import re
import time


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


class MantaDataScrape:
    CLASSES = {
        "reviews_span": "numerals ng-binding",
    }

    IDS = {
        "claim_span": "verified-business",
        "contact_container": "contactContent",
        "datails_container": "detailsContent",
        "reviews_container": "reviewsContent",
    }

    def __init__(self, html: str = None):
        if not html:
            with open("mapquest.html", "r") as f:
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

        print(containers_found)

        return all(containers_found)

    def parse(self):
        self.summary["name"] = self.get_name()
        self.summary["email"] = self.get_email()
        self.summary["claimed"] = self.is_claim()
        self.summary["starts"] = self.get_starts()
        # self.summary["location"] = self.get_location()
        self.summary["accept_credit_card"] = self.get_accept_credit_card()
        self.summary["phone"] = self.get_phone()
        # self.summary["website"] = self.get_website()
        # self.summary["years"] = self.get_years_from_established()
        # self.summary["employees"] = self.get_employees()
        # self.summary["contacts"] = self.get_contacts()
        self.summary["reviews"] = self.get_reviews()

    def get_name(self) -> str:
        return self.soup.find("div", {"class": "header-wrapper"}).text.strip()

    def get_email(self) -> str:
        email = ""
        email_container = self.soup.find("email", {"class": "ng-scope"})
        if email_container:
            a_tag = email_container.find("a", {"class": "ng-scope"})
            if a_tag:
                email = a_tag["href"].replace("mailto:", "")
        return email

    def is_claim(self) -> bool:
        return True if "verified" in self.soup.find("div", {
            "id": self.IDS.get("claim_span")}).text.strip().lower() else False

    def get_accept_credit_card(self) -> bool:
        payments = self.soup.find_all("li", {"itemprop": "paymentAccepted"})
        payments = set([payment.text.strip().lower() for payment in payments])
        no_credit_cards = set(["check", "cash"])
        credit_cards = payments - no_credit_cards
        return True if credit_cards else False

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
        return self.soup.find("p", text=re.compile(r'([1-9]{3}) [1-9]{3}-[1-9]{4}')).text.strip()

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
        return self.soup.find("span", {"class": self.CLASSES.get("reviews_span")}).text.strip().replace(" Reviews", "")

    def get_starts(self):
        starts = ""
        stars_container = self.soup.find("meta", {"itemprop": "ratingValue"})
        if stars_container:
            starts = stars_container.text.strip()

        return starts
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
