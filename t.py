import pymongo

myclient = pymongo.MongoClient(
    "mongodb+srv://eduardo:05120714@prometeocluster.rk11h.mongodb.net/prometeo_db?retryWrites=true&w=majority")
mydb = myclient["prometeo_db"]
mycol = mydb["fetch_attempts"]

myquery = {"CATEGORY": 'Fire and Chimney'}

x = mycol.delete_many(myquery)

print(x.deleted_count, " documents deleted.")
