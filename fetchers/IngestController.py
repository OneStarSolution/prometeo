import yaml


class IngestController:

    CONFIG_FILE_NAME = ""

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError()

    def formatDownStreamScope(self, current):
        """
        Send the scope to downstream classes (fetcher controllers)
        """
        raise NotImplementedError()

    @classmethod
    def instanciate_config(cls, config):
        raise NotImplementedError()

    @classmethod
    def load_config(cls):
        with open(cls.CONFIG_FILE_NAME, 'r') as stream:
            return cls.instanciate_config(yaml.load(stream))

    def addScope(self, name, scope):
        if not isinstance(scope, dict):
            raise Exception("Scope is Incorrectly built")
        if "caseClass" not in scope:
            scope["caseClass"] = self.getCaseDBClass()
        self._scopes[name] = scope

    def getCurrentScope(self):
        if self.scope:
            return self._scopes.get(self.scope)
        return {}

    def getAllScopesNames(self):
        return list(self._scopes.keys())

    def setCurrentScope(self, name):
        if name in self._scopes:
            self.scope = name
            return True
        return False

    def resetCurrentScope(self, **kwargs):
        """Resets current scope the first one in a range"""
        self.current = self.getCurrentScope().get("start", 0)-1

    def get_config_case_numbers(self):
        """Return a generator of a dict of cases left to crawl from config,
        exlcuidng all invalid cases, cases in database, and if not recrawling,
        recent crawled cases
        """
        # Get a dictionary of all cases for this county
        cases_on_db = self.get_case_numbers_on_db()
        # exclude the ones we have checked
        cases_ignore = self.get_all_invalid_case_numbers()
        # get a dictionary of all cases that were recently crawled
        cases_recently_crawled = self.get_recently_crawled_case_numbers()

        for scopename in self.getAllScopesNames():
            self.setCurrentScope(scopename)
            self.resetCurrentScope()
            for caseno in self:
                # Create list of verifcations
                verifications = []
                # check if the current case is on the db.
                verifications.append(cases_on_db.get(caseno))
                # Check if the current case is invalid
                verifications.append(cases_ignore.get(caseno))
                # check if the currently case was crawled recently
                verifications.append(cases_recently_crawled.get(caseno))
                # if the current case does not fit at least one
                # verification, add it to dict
                if not any(verifications):
                    yield caseno

    def get_needed_case_numbers(self):
        return []
        # Get a dictionary of all cases for this county
        cases_on_db = self.get_case_numbers_on_db()
        # exclude the ones we have checked
        if self.ignore_all_invalids:
            cases_ignore = self.get_all_invalid_case_numbers()
        else:
            cases_ignore = self.get_invalid_case_numbers()
        # get a dictionary of all cases that were recently crawled.
        cases_recently_crawled = self.get_recently_crawled_case_numbers()

        # Getting cases for fast crawl if applicable
        if self.getCaseDBClass() in self.rapid_recrawl:
            cases_to_fast_crawl = self.get_recently_created_for_fast_crawl()

        for scopename in self.getAllScopesNames():
            self.setCurrentScope(scopename)
            self.resetCurrentScope()
            for caseno in self:
                # check if the current case is on the db.
                on_db = cases_on_db.get(caseno)
                # check if the currently case was crawled recently
                recently_crawled = cases_recently_crawled.get(caseno)
                # Check if the current case is invalid
                invalid = cases_ignore.get(caseno)
                # if the current case is not on the db (or on the db and not open)
                # and is not valid and wasn't recently crawled.
                # crawl that case.
                if not on_db and not invalid and not recently_crawled:
                    yield dict(self.formatDownStreamScope(caseno))

                # Rapid recrawl logic
                if self.getCaseDBClass() in self.rapid_recrawl:
                    case_in_fast_crawl = cases_to_fast_crawl.get(caseno)
                    if case_in_fast_crawl:
                        yield dict(self.formatDownStreamScope(caseno))
