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
            caseType = self.getCurrentScope().get("caseType", "")
            caseYear = self.getCurrentScope().get("caseYear", "")
            caseNumber = str(self.current).zfill(2)

            return f"{caseType}-{caseYear}{caseNumber}"

    @classmethod
    def instanciate_config(cls, config):
        """Creates ingest controller and appends all scopes in config
        :param config: yaml config file in dict form
        """
        ictl = cls()
        states = config.get("States")
        for state in states:
            state_range = state.get("Range")
            scope = {}
            scope["state"] = state.get('State')
            scope["start"] = state_range.get("begin", 0)
            scope["end"] = state_range.get("end", 0)
            print(scope)
            ictl.addScope(f'{cls.SOURCE}_{state}', scope)
        return ictl

    def formatDownStreamScope(self, current):
        """Creates scope from current case number
        :param current: case number of current iteration
        """
        scope = self.getCurrentScope()
        if not scope:
            scope = {}

        caseType = self.getCurrentScope().get("caseType", "")
        caseYear = self.getCurrentScope().get("caseYear", "")

        prefix = "{}-{}".format(caseType, caseYear)
        current = re.sub("^{}".format(prefix), "", current)
        scope.update({"caseNumber": current})
        return scope


def run_sample():
    ic = YELPIngestController.load_config()
    cases = []

    for case in ic.get_needed_case_numbers():
        cases.append(case)
        if len(cases) > 3:
            break

    for case in cases:
        print("Case ->", case)
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
