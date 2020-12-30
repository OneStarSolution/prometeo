import logging
import re

from bs4 import BeautifulSoup
from fetchers.FetcherDocument import FetcherDocument


# This is not the robust regex, it's being used for test porpuses only.
URL_REGEX = r"\w*.[com|net]+"

BUSINESS_OWNER_REGEX = r'^businessOwner[\w-]+'


class YELPFetcherDocument(FetcherDocument):
    DOMAIN = "YELP"
    CONTACT_INFO_INDEX = -1
    AMENITIES_INDEX = 8

    CLASSES = {
        'title': "lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy",
        'contact_info': "lemon--section__373c0__fNwDM margin-b3__373c0__q1DuY border-color--default__373c0__3-ifU",
        'amenities': 'lemon--section__373c0__fNwDM margin-t4__373c0__1TRkQ padding-t4__373c0__3hVZ3 border--top__373c0__3gXLy border-color--default__373c0__3-ifU',
        'claimed': 'lemon--span__373c0__3997G text__373c0__2Kxyz claim-text--dark__373c0__xRoSM text-color--blue-regular__373c0__QFzix text-align--left__373c0__2XGa- text-weight--semibold__373c0__2l0fe text-bullet--after__373c0__3fS1Z text-size--large__373c0__3t60B',
        'response_stats': 'lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--green__373c0__OGSCR text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--large__373c0__3t60B'
    }

    def __init__(self, url):
        self.domain = self.DOMAIN
        self.url = url
        self.summary = {}

    def _verify(self, soup: BeautifulSoup, **kwargs):

        try:
            # Find the title
            soup.find('h1', {'class': self.CLASSES['title']})

            # Find the contact section
            results = soup.find_all(
                'section', {'class': self.CLASSES['contact_info']})

            # Contact section use to be the second
            if not results:
                raise Exception("Contact info is missing")

        except AttributeError:
            print("Title or contact section could not be located")

        return soup

    def parse_summary(self, soup: BeautifulSoup):
        # Get website
        self.summary['website'] = self.get_website(soup)

        # Get accept_card
        self.summary['accept_cards'] = self.get_accept_cards(soup)

        # Get is_claimed
        self.summary['is_claimed'] = self.is_claimed(soup)

        response_time, response_rate = self.get_response_stats(soup)

        self.summary['response_time'] = response_time or None

        self.summary['response_rate'] = response_rate or None

        contact_name, contact_role = self.get_contact_info(soup)

        self.summary['contact_name'] = contact_name or None

        self.summary['contact_role'] = contact_role or None

    def get_website(self, soup: BeautifulSoup):
        # Find the contact section (last one)
        contact_sections = soup.find_all(
            'section', {'class': self.CLASSES['contact_info']})

        # Find the urls in the contact section
        links = []
        for contact_section in contact_sections:
            possible_urls = contact_section.find_all('a')
            if possible_urls:
                links.extend(possible_urls)

        # As links could content urls that are not the main url of the business
        # we would take only the first link displayed in the section
        website = self.get_business_website(links)

        return website

    def get_business_website(self, links: list):
        pattern = re.compile(URL_REGEX)

        for link in links:
            match = re.search(pattern, link.text)
            if match:
                return match.group(0)

        return None

    def get_accept_cards(self, soup: BeautifulSoup):
        ameneties = soup.find_all(
            'section', {'class': self.CLASSES['amenities']})

        if not ameneties:
            return None

        if self.AMENITIES_INDEX >= len(ameneties):
            return False

        spans = ameneties[self.AMENITIES_INDEX].find_all('span')

        for span in spans:
            if span.text.lower() == 'accepts credit cards':
                return True

        return False

    def is_claimed(self, soup: BeautifulSoup):
        claim_span = soup.find('span', {'class': self.CLASSES['claimed']})

        return True if claim_span else False

    def get_response_stats(self, soup: BeautifulSoup):
        paragraphs = soup.find_all(
            'p', {'class': self.CLASSES['response_stats']})

        if not paragraphs or paragraphs and len(paragraphs) != 2:
            return None, None

        return paragraphs[0].text, paragraphs[1].text

    def get_contact_info(self, soup: BeautifulSoup):
        container = soup.find(
            'div', {'aria-labelledby': re.compile(BUSINESS_OWNER_REGEX)})

        if not container:
            print("There is no a container of business info")
            return None, None

        paragraphs = container.find_all('p', recursive=True)

        if not paragraphs or paragraphs and len(paragraphs) != 3:
            print(
                "There are no paragraphs or there are less/more than expected in the business owner container")
            return None, None

        return paragraphs[1].text,  paragraphs[2].text
