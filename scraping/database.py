import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

pymongo_client = pymongo.MongoClient(os.getenv("MONGODB_URL"))
pymongo_db = pymongo_client[os.getenv("MONGODB_DATABASE")]
pymongo_col = pymongo_db[os.getenv("MONGODB_COLLECTION")]

def add_row(user_data):
    pymongo_col.insert_one(user_data)

def is_uuid_already_scraped(uuid):
    exists_items = pymongo_col.count_documents({
        "uuid": uuid
    })
    
    already_exists = exists_items > 0

    if already_exists:
        print(f"User {uuid} already scraped")

    return already_exists