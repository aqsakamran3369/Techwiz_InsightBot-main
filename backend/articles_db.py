from pymongo import MongoClient
import json
import os

# ---------- MongoDB Connection ----------
MONGO_URI = "mongodb+srv://thewebwiz23:TheWebWiz2988@cluster0.8edmm.mongodb.net/insightbot_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.insightbot_db
articles_collection = db.articles

# ---------- Load Articles from JSON ----------
TRAINING_JSON = "data/preprocessed/training_articles.json"
TESTING_JSON = "data/preprocessed/testing_articles.json"

def load_articles(json_path, dataset_type):
    if not os.path.exists(json_path):
        print(f"⚠️ File not found: {json_path}")
        return []

    with open(json_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    for art in articles:
        art["dataset_type"] = dataset_type
        art.pop("_id", None)  # avoid duplicate _id issues
    return articles

training_articles = load_articles(TRAINING_JSON, "training")
testing_articles = load_articles(TESTING_JSON, "testing")
all_articles = training_articles + testing_articles

# ---------- Insert into MongoDB ----------
if all_articles:
    # Optional: avoid duplicates by URL
    for art in all_articles:
        if not articles_collection.find_one({"url": art["url"]}):
            articles_collection.insert_one(art)
    print(f"✅ Inserted/Updated {len(all_articles)} articles into MongoDB!")
else:
    print("⚠️ No articles to insert.")

# ---------- Fetch & Display ----------
print("\n📄 Sample Articles from DB:")
for art in articles_collection.find({}, {"_id": 0}).limit(5):
    print(f"{art['dataset_type'].upper()} | {art['url']} | {art['language']} | {art['title'][:50]}...")
