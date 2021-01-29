import gzip
import base64
import hashlib
import datetime

from utils.CleanUtils import CleanUtils


class FetcherDocument:
    def __init__(self, _id, phone, url, country, search_location, **kwargs):
        self.source = None
        self.md5 = None
        self.data = None
        self.url = url
        clean_phone = CleanUtils.clean_phone(phone)
        self.id = _id if _id != phone else clean_phone
        self.phone = clean_phone
        self.display_phone = phone
        self.country = country
        self.search_location = search_location
        now = datetime.datetime.utcnow()
        self.created = kwargs.get("created", now)
        self.category = kwargs.get("category", None)
        self.last_crawled = kwargs.get('last_crawled', now)
        self.last_modified = kwargs.get("last_modified", now)

    def setData(self, file, **kwargs):
        driver = kwargs.get("driver")
        md5_hash = hashlib.md5(file.encode('utf-8')).hexdigest()
        self.md5 = md5_hash
        self.data = self.gzip(file)

    def gunzip(self, contents):
        return gzip.decompress(base64.b64decode(contents))

    def gzip(self, contents):
        gzipped = base64.b64encode(gzip.compress(contents.encode('utf-8')))

        return gzipped.decode("utf-8")

    def to_dict(self):
        document = {
            "SOURCE": self.source,
            "ID": self.id,
            "MD5": self.md5,
            "RAW": self.data,
            "LAST_MODIFIED": self.last_modified,
            "CREATED": self.created,
            "URL": self.url,
            "PHONE": self.phone,
            "COUNTRY": self.country,
            "SEARCH_LOCATION": self.search_location,
            "CATEGORY": self.category,
            "LAST_CRAWLED": self.last_crawled,
        }

        return document

    def __repr__(self):
        return str(self.to_dict())

    def __eq__(self, other):
        if not isinstance(other, FetcherDocument):
            return False

        if self.md5 != other.md5:
            return False
        return True
