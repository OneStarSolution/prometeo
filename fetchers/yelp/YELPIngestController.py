import re
import os

from fetchers.yelp.YELPFetcherController import YELPFetcherController
from fetchers.IngestController import IngestController


class YELPIngestController(IngestController):

    SOURCE = "YELP"
    CONFIG_FILE_NAME = "YELP_config.yaml"

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
    def instanciate_config(cls, config):
        """Creates ingest controller and appends all scopes in config
        :param config: yaml config file in dict form
        """
        ictl = cls()
        states = config.get("States")
        for state in states:
            state_name = state.get('State')
            state_range = state.get("Range")
            scope = {}
            scope["state"] = state_name
            scope["start"] = state_range.get("begin", 0)
            scope["end"] = state_range.get("end", 0)
            ictl.addScope(f'{cls.SOURCE}_{state_name}', scope)
        return ictl


def run_sample():
    ic = YELPIngestController.load_config()
    cases = []

    for case in ic.get_needed_case_numbers():
        cases.append(case)

    for case in cases:
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


run_sample()
