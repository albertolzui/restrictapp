def get_database():
    from pymongo import MongoClient
    import pymongo

    # provide MongoDB atlas url to connect to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://<albertolz>:<Amala_2022_begrenzen+>@restrictapp-one.mongodb.net/restrictapp-one"

    client = MongoClient(CONNECTION_STRING)

    # create database
    return client['restrictapp-one']

restrictapp_one = get_database()
collection_name = restrictapp_one['country_code_name_collection']

country_to_code = {
    "Argentina": "AR",
    "Belgium": "BE",
    "China": "CN",
    "Germany": "DE",
    "Ghana": "GH",
    "Nigeria": "NG"
}
collection_name.insert_one([country_to_code])



if __name__ == "main":
    restrictapp_one = get_database()
