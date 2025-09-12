import os
import json
from pymongo import MongoClient

# ================== CONFIG ==================
EXTRACTED_DIR = "data/extracted_multilang"
MONGO_URI = "mongodb+srv://muskankamran3369:muskurahat2328U@cluster0.fxk1min.mongodb.net/insightbot_db?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "insightbot_db"
COLLECTION_NAME = "articles"
# ============================================

def insert_articles_to_mongo(file_path, split):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    cleaned_articles = []
    for article in articles:
        article.pop("_id", None)  # remove old Mongo _id
        if "language" in article:  # rename only if exists
            article["lang"] = article.pop("language")
        article["dataset_type"] = split
        cleaned_articles.append(article)

    # clear old docs of this split
    collection.delete_many({"dataset_type": split})

    if cleaned_articles:
        result = collection.insert_many(cleaned_articles, bypass_document_validation=True)
        print(f"✅ Inserted {len(result.inserted_ids)} {split} articles into MongoDB")
    else:
        print(f"⚠️ No articles in {file_path}")

if __name__ == "__main__":
    insert_articles_to_mongo(os.path.join(EXTRACTED_DIR, "training_articles.json"), "training")
    insert_articles_to_mongo(os.path.join(EXTRACTED_DIR, "testing_articles.json"), "testing")
    print("🎉 Done! Both training & testing articles inserted into MongoDB.")
