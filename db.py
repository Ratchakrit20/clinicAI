from pymongo import MongoClient
def get_mongo_collection():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017")

    # Access a specific database
    db = client["api"]

    # Access a specific collection within the database
    collection = db["restapi"]

    return collection