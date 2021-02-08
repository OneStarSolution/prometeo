import re
import os

from utils.yelp_token import get_request_available
from fetchers.IngestController import IngestController
from fetchers.yelp.YELPFetcherController import YELPFetcherController


class YELPIngestController(IngestController):

    SOURCE = "YELP"
    ZIPCODES_CONFIG_FILE_NAME = "YELP_config.yaml"
    CATEGORIES_CONFIG_FILE_NAME = "YELP_categories.yaml"

    @classmethod
    def instanciate_config(cls, categories_config):
        """Creates ingest controller and appends all scopes in zipcodes_config
        :param zipcodes_config: yaml zipcodes_config file in dict form
        :categories_config: yaml categories_config file dict form
        """
        ictl = cls()
        categories = categories_config.get("Categories")
        target_categories = [
            category for category in categories if categories[category]]

        for category in target_categories:
            scope = {'category': category}
            print(scope)
            ictl.addScope(
                f'{cls.SOURCE}_{category}', scope)

        return ictl

    def get_needed_case_numbers(self):
        """Return a generator of a dict of cases left to crawl from config,
        exlcuidng all invalid cases, cases in database, and if not recrawling,
        recent crawled cases
        """
        cases_recently_crawled = self.get_recently_crawled_zipcodes()

        limit = get_request_available()
        print("limit", limit)
        i = 0

        for scopename in self.get_all_scope_names():
            self.setCurrentScope(scopename)
            self.resetCurrentScope()
            valid_zipcodes = self.get_locations()
            for zipcode in valid_zipcodes:
                if i >= limit:
                    print("No more queries available")
                    raise StopIteration
                # check if the currently case was crawled recently
                recently_crawled = (
                    zipcode, self.getCurrentScope().get('category')) in cases_recently_crawled

                # if the current zipcode was not crawled recently, crawl that case.
                if not recently_crawled:
                    scope = self.getCurrentScope()

                    if not scope:
                        scope = {}

                    scope.update({"zipcode": zipcode})
                    i += 1
                    yield dict(scope)


def run_sample():
    ic = YELPIngestController.load_config()
    cases = []

    for case in ic.get_needed_case_numbers():
        cases.append(case)
    print(len(cases))
    for case in cases[-3:]:
        print("Task ->", case)
    # fetcher = YELPFetcherController()
    # fetcher.setScope(**case)
    # print(fetcher.getCaseIDString())
    # document = None
    # try:
    #     document = fetcher.run()
    # except Exception as e:
    #     print(e)
    #     continue
    # if document:
    #     print(document)
    #     fetcher.save(document)


# run_sample()
