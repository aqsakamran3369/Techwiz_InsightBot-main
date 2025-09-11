from pymongo import MongoClient
import json, os

# Replace <db_password> with your actual password
MONGO_URI = "mongodb+srv://thewebwiz23:TheWebWiz2988@cluster0.8edmm.mongodb.net/insightbot_db?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client.insightbot_db
articles_collection = db.articles  # collection for training + testing

# Paths to extracted data
EXTRACTED_DIR = "data/extracted_multilang"

for split in ["training", "testing"]:
    file_path = os.path.join(EXTRACTED_DIR, f"{split}_articles.json")
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    for art in articles:
        art["dataset_type"] = split
        art.pop("_id", None)  # remove old MongoDB IDs

    if articles:
        result = articles_collection.insert_many(articles)
        print(f"✅ Inserted {len(result.inserted_ids)} {split} articles into MongoDB")
    else:
        print(f"⚠️ No {split} articles to insert.")

# from pymongo import MongoClient
# import json, os

# # MongoDB connection
# # client = MongoClient(
# #     "mongodb+srv://muskankamran3369:muskurahat2328U@cluster0.fxk1min.mongodb.net/insightbot_db?retryWrites=true&w=majority&appName=Cluster0"
# # )
# client = MongoClient(
#     "mongodb+srv://muskankamran3369:muskurahat2328U@cluster0.fxk1min.mongodb.net/insightbot_db?retryWrites=true&w=majority&appName=Cluster0"
# )
# db = client.insightbot_db
# articles_collection = db.articles  # single collection (training + testing)

# # Paths to extracted data
# EXTRACTED_DIR = "data/extracted_multilang"

# for split in ["training", "testing"]:
#     file_path = os.path.join(EXTRACTED_DIR, f"{split}_articles.json")
#     with open(file_path, "r", encoding="utf-8") as f:
#         articles = json.load(f)

#     for art in articles:
#         art["dataset_type"] = split
#         art.pop("_id", None)  # remove old MongoDB _id

#     if articles:
#         result = articles_collection.insert_many(articles)
#         print(f"✅ Inserted {len(result.inserted_ids)} {split} articles into MongoDB")
#     else:
#         print(f"⚠️ No {split} articles to insert.")
