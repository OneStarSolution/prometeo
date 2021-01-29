from pymongo import UpdateOne

from db.PrometeoDB import PrometeoDB


class FetcherController:
    def save(self, documents):
        document_dicts = []
        for document in documents:
            if not isinstance(document, dict):
                document = document.to_dict()

            document['_id'] = document.get('ID')
            del document['ID']
            document_dicts.append(document)

        with PrometeoDB() as db:
            businesses = db.get_businesses()
            operations = [
                UpdateOne({"_id": doc.get("_id")}, {"$set": doc}, upsert=True) for doc in document_dicts
            ]
            result = businesses.bulk_write(operations)
            print(result)
