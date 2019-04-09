import pymongo
from pymongo.collection import Collection


def mongodb_insert():
    with open("C:/Users/admin/Desktop/100.txt", "r") as f:
        for each_line in f:
            ls = each_line.replace("\n", "").split("----")
            user_dict = {}
            client = pymongo.MongoClient(host='localhost', port=27017)
            db = client['huya']
            id_collection = Collection(db, 'huya_users')
            user_dict["user_name"] = ls[0]
            user_dict["user_password"] = ls[1]
            id_collection.insert(user_dict)


def get_random_info():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['huya']
    id_collection = Collection(db, 'huya_users')
    info = id_collection.find_one_and_delete({})
    user_name = info["user_name"]
    password = info["user_password"]
    return user_name, password


mongodb_insert()
