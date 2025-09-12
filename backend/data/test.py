import json
from pymongo import MongoClient

# ================== CONFIG ==================
MONGO_URI = "mongodb+srv://muskankamran3369:muskurahat2328U@cluster0.fxk1min.mongodb.net/insightbot_db?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "insightbot_db"
COLLECTION_NAME = "articles"
OUTPUT_FILE = "all_articles.json"
# ============================================

def export_articles_to_json():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # saare documents uthao
    articles = list(collection.find({}, {"_id": 0}))  # _id hata diya

    if not articles:
        print("⚠️ No articles found in MongoDB.")
        return

    # file me dump karo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Exported {len(articles)} articles into {OUTPUT_FILE}")

if __name__ == "__main__":
    export_articles_to_json()
