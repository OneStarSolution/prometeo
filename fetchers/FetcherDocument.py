import gzip
import base64
import hashlib

from bs4 import BeautifulSoup


class FetcherDocument:
    def setData(self, file, **kwargs):
        driver = kwargs.get("driver")
        soup = BeautifulSoup(file, 'html.parser')
        root = self._verify(soup, **kwargs)
        data = str(root)
        md5_hash = hashlib.md5(data.encode('utf-8')).hexdigest()
        self.md5 = md5_hash
        self.data = self.gzip(data)

        self.parse_summary(root)

    def gunzip(self, contents):
        return gzip.decompress(base64.b64decode(contents))

    def gzip(self, contents):
        gzipped = base64.b64encode(gzip.compress(contents.encode('utf-8')))

        return gzipped.decode("utf-8")
