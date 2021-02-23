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

    def __init__(self):
        html = ""
        with open("manta.html", "r") as f:
            html = f.read()

        self.soup = BeautifulSoup(html)
        self.summary = {}

    def verify(self):
        ask_captcha_container = self.soup.find(
            "h2", {"class": self.CLASSES.get("ask_captcha_container")})
        ask_captcha_text = "please complete the security check to access"

        if ask_captcha_container and ask_captcha_text in ask_captcha_container:
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


m = MantaDataScrape()
m.parse()
print(m.summary)
