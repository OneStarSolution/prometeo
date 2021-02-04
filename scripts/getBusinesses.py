import pandas as pd

from db.PrometeoDB import PrometeoDB


def getBusinesses(query=None):
    with PrometeoDB() as db:
        businesses = db.get_businesses()
        query = {} if not query else query
        result = [doc for doc in businesses.find(query, {'RAW': 0, 'MD5': 0})]
        df = pd.DataFrame(result)
        df.to_csv("YELLOWPAGES_ALL.csv")


query = {
    "SOURCE": "YELLOWPAGES"
}
getBusinesses()
