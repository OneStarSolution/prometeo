import re
import os

from fetchers.yellowpages.YellowPagesFetcherController import YellowPagesFetcherController
from fetchers.IngestController import IngestController


class YellowPagesIngestController(IngestController):

    SOURCE = "YellowPages"
    ZIPCODES_CONFIG_FILE_NAME = "YellowPages_config.yaml"
    CATEGORIES_CONFIG_FILE_NAME = "YellowPages_categories.yaml"

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


def run_sample():
    ic = YellowPagesIngestController.load_config()
    cases = []

    for case in ic.get_needed_case_numbers():
        cases.append(case)
    print(len(cases))
    for case in cases[-3:]:
        print("Task ->", case)
    # fetcher = YellowPagesFetcherController()
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
