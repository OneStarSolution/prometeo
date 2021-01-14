import re
import os

from fetchers.YELP.YELPFetcherController import YELPFetcherController
from fetchers.IngestController import IngestController


class YELPIngestController(IngestController):

    SOURCE = "YELP"
    ZIPCODES_CONFIG_FILE_NAME = "YELP_config.yaml"
    CATEGORIES_CONFIG_FILE_NAME = "YELP_categories.yaml"

    def __next__(self):
        """Iterates over scopes to yield case numbers
        """
        if self.current >= self.getCurrentScope().get("end", 0):
            raise StopIteration
        else:
            self.current += 1
            # caseType = self.getCurrentScope().get("caseType", "")
            # caseYear = self.getCurrentScope().get("caseYear", "")
            caseNumber = str(self.current).zfill(5)

            return f"{caseNumber}"

    @classmethod
    def instanciate_config(cls, zipcodes_config, categories_config):
        """Creates ingest controller and appends all scopes in zipcodes_config
        :param zipcodes_config: yaml zipcodes_config file in dict form
        :categories_config: yaml categories_config file dict form
        """
        ictl = cls()
        states = zipcodes_config.get("States")
        categories = categories_config.get("Categories")
        target_categories = [
            category for category in categories if categories[category]]

        for state in states:
            for category in target_categories:
                state_name = state.get('State')
                state_ranges = state.get("Ranges")

                for i, state_range in enumerate(state_ranges):
                    print(state_range)
                    scope = {
                        'category': category,
                        "state": state_name,
                        "start": state_range.get("Range").get("begin", 0),
                        "end": state_range.get("Range").get("end", 0),
                    }

                    ictl.addScope(
                        f'{cls.SOURCE}_{state_name}_{category}_{i}', scope)

        return ictl


def run_sample():
    ic = YELPIngestController.load_config()
    cases = []

    for case in ic.get_needed_case_numbers():
        cases.append(case)
        if len(cases) > 3000:
            break

    for case in cases[-5:]:
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
