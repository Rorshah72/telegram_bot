from config import tokenBot, url, mongo_pass
from pymongo import MongoClient

#connect mongo
cluster = MongoClient(f"mongodb+srv://telegram_bot:{mongo_pass}@cluster0.gcizq3k.mongodb.net/?retryWrites=true&w=majority")
db = cluster["telegram_bot"]
collection = db['data_users_info']



results = collection.find({"telegramid": "@BurykM"})

for item in results:
    print(item.get("steamid"))

#update data in database
#collection.update_one({"telegramid": "", "steamid": ""}, {"$set": {"telegramid": ""}})

#delete data in database
#collection.delete_one({"telegramid": "", "steamid": ""})

cluster.close()