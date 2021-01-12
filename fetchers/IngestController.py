import os
import yaml
import datetime

from db.PrometeoDB import PrometeoDB


class IngestController:

    CONFIG_FILE_NAME = ""
    SOURCE = ""

    def __init__(self, *args, **kwargs):
        self._scopes = {}
        self.scope = None
        self.current = 0
        self.db = PrometeoDB()

    def __del__(self):
        self.db.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError()

    def get_source_db_name(self):
        if not self.SOURCE:
            raise FetcherError("Unassigned SOURCE name variable")
        return self.SOURCE

    def formatDownStreamScope(self, current):
        """
        Send the scope to downstream classes (fetcher controllers)
        """
        raise NotImplementedError()

    @classmethod
    def instanciate_config(cls, config):
        raise NotImplementedError()

    @classmethod
    def config_file_path(cls):
        """Declares name of config file"""

        if not cls.CONFIG_FILE_NAME:
            raise FetcherError("Unassigned CONFIG_FILE_NAME class variable")

        return os.path.join(os.path.dirname(__file__), cls.SOURCE, cls.CONFIG_FILE_NAME)

    @classmethod
    def load_config(cls):
        filename = cls.config_file_path()
        with open(filename, 'r') as stream:
            return cls.instanciate_config(yaml.load(stream, Loader=yaml.FullLoader))

    def addScope(self, name, scope):
        if not isinstance(scope, dict):
            raise Exception("Scope is Incorrectly built")
        if "SOURCE" not in scope:
            scope["SOURCE"] = self.get_source_db_name()
        self._scopes[name] = scope

    def getCurrentScope(self):
        if self.scope:
            return self._scopes.get(self.scope)
        return {}

    def get_all_scope_names(self):
        return list(self._scopes.keys())

    def setCurrentScope(self, name):
        if name in self._scopes:
            self.scope = name
            return True
        return False

    def resetCurrentScope(self, **kwargs):
        """Resets current scope the first one in a range"""
        self.current = self.getCurrentScope().get("start", 0)-1

    def get_recently_crawled_zipcodes(self):
        """
        Check the fetched collection and get a list of case records that have not been crawled in 60 days.
        """
        attemps = self.db.get_fetch_attempts()
        reference_time = datetime.datetime.today() - datetime.timedelta(days=15)
        query = {"SOURCE": self.get_source_db_name(),
                 "TIME": {"$gte": reference_time}}

        recently_crawled = attemps.find(
            query, {"LOCATION": 1}, no_cursor_timeout=True)

        arr = [x.get("LOCATION") for x in recently_crawled]
        set_zipcodes = set(arr)

        return set_zipcodes

    def get_needed_case_numbers(self):
        """Return a generator of a dict of cases left to crawl from config,
        exlcuidng all invalid cases, cases in database, and if not recrawling,
        recent crawled cases
        """

        # # Get a dictionary of all cases for this county
        # cases_on_db = self.get_case_numbers_on_db()
        # # exclude the ones we have checked
        # if self.ignore_all_invalids:
        #     cases_ignore = self.get_all_invalid_case_numbers()
        # else:
        #     cases_ignore = self.get_invalid_case_numbers()
        # get a dictionary of all cases that were recently crawled.
        cases_recently_crawled = self.get_recently_crawled_zipcodes()
        print("rrecently", cases_recently_crawled)

        for scopename in self.get_all_scope_names():
            print(scopename)
            self.setCurrentScope(scopename)
            self.resetCurrentScope()
            for zipcode in self:
                # check if the currently case was crawled recently
                recently_crawled = zipcode in cases_recently_crawled

                # if the current zipcode was not crawled recently, crawl that case.
                if not recently_crawled:
                    scope = self.getCurrentScope()

                    if not scope:
                        scope = {}

                    scope.update({"zipcode": zipcode})
                    yield dict(scope)
