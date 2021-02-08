import os
import yaml
import datetime

from db.PrometeoDB import PrometeoDB


class IngestController:

    ZIPCODES_CONFIG_FILE_NAME = ""
    CATEGORIES_CONFIG_FILE_NAME = ""
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
            raise Exception("Unassigned SOURCE name variable")
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
    def config_file_paths(cls):
        """Declares name of config file"""

        if not cls.ZIPCODES_CONFIG_FILE_NAME:
            raise FetcherError(
                "Unassigned ZIPCODES_CONFIG_FILE_NAME class variable")

        if not cls.CATEGORIES_CONFIG_FILE_NAME:
            raise FetcherError(
                "Unassigned CATEGORIES_CONFIG_FILE_NAME class variable")

        return os.path.join(os.path.dirname(__file__), cls.SOURCE.lower(),
                            cls.CATEGORIES_CONFIG_FILE_NAME)

    @classmethod
    def load_config(cls):
        categories_filename = cls.config_file_paths()
        with open(categories_filename, 'r') as categories_config:
            return cls.instanciate_config(
                yaml.load(categories_config, Loader=yaml.FullLoader))

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
            query, {"LOCATION": 1, "CATEGORY": 1})

        arr = [(x.get("LOCATION"), x.get("CATEGORY"))
               for x in recently_crawled]
        set_zipcodes = set(arr)

        return set_zipcodes

    def get_locations(self):

        with open('valid_zipcodes.csv', 'r') as f:
            lines = [line.replace('\n', '') for line in f.readlines()]

        with open('CAN_city.csv', 'r') as f:
            canada_lines = [line.replace('\n', '')[:-1]
                            for line in f.readlines()]

        for line in lines + canada_lines:
            yield line

    def get_needed_case_numbers(self):
        """Return a generator of a dict of cases left to crawl from config,
        exlcuidng all invalid cases, cases in database, and if not recrawling,
        recent crawled cases
        """
        cases_recently_crawled = self.get_recently_crawled_zipcodes()

        i = 0

        for scopename in self.get_all_scope_names():
            self.setCurrentScope(scopename)
            self.resetCurrentScope()
            valid_zipcodes = self.get_locations()
            print(scopename)
            for zipcode in valid_zipcodes:
                # check if the currently case was crawled recently
                recently_crawled = (
                    zipcode, self.getCurrentScope().get('category')) in cases_recently_crawled

                # if the current zipcode was not crawled recently, crawl that case.
                if not recently_crawled:
                    scope = self.getCurrentScope()

                    if not scope:
                        scope = {}

                    scope |= {"country": "USA" if zipcode.isnumeric() else "CA",
                              "location": zipcode.zfill(5) if zipcode.isnumeric() else zipcode}
                    i += 1
                    yield dict(scope)
