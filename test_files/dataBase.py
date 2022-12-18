from config import mongo_pass
from pymongo import MongoClient
from users import Users


class DataBase:
    def __init__(self):
        cluster = MongoClient(f"mongodb+srv://telegram_bot:{mongo_pass}@cluster0.gcizq3k.mongodb.net/?retryWrites=true&w=majority")

        self.db = cluster["telegram_bot"]
        self.users = self.db["Users"]
        self.question = self.db["Questions"]

        self.question_count = len(list(self.question.find({})))


    def get_user(self,chatid):
        user = self.users.find_one({"chatid": chatid})

        if user is not None:
            return user

        user = {
            "chatid": chatid,
            "is_passing": False,
            "is_passed": False,
            "question_index": None,
            "answers": []
        }

        self.users.insert_one(user)
        return user


    #set user
    def set_user(self,chatid, update):
        self.users.update_one({"chatid": chatid}, {"$set": update})


    #get question in database
    def get_question(self, index):
        return self.question.find_one({"id": index})



