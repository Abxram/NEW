from pymongo import MongoClient
import json

def insert_data_to_mongo(df, db_name, collection_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    collection = db[collection_name]

    collection.delete_many({})  # Clean existing
    records = json.loads(df.to_json(orient='records'))
    collection.insert_many(records)
    print(f"✅ Inserted {len(records)} records into MongoDB collection '{collection_name}'")
