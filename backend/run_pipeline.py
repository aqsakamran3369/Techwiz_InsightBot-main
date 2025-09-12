import subprocess
import sys
import os
import json
import schedule
import time
from pymongo import MongoClient

# MongoDB connection (local, change if needed)
client = MongoClient("mongodb+srv://muskankamran3369:muskurahat2328U@cluster0.fxk1min.mongodb.net/insightbot_db?retryWrites=true&w=majority&appName=Cluster0")
db = client.insightbot_db
articles_collection = db.articles

# ------------------ Helpers ------------------ #
def run_step(command, step_name):
    print(f"🚀 Running {step_name}...")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Error in {step_name}. Stopping pipeline.")
        sys.exit(1)
    print(f"✅ {step_name} completed.\n")

# def insert_articles_to_mongo(file_path, split):
#     if os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as f:
#             articles = json.load(f)

#         # Remove Mongo _id field if exists
#         for article in articles:
#             article.pop("_id", None)
#             article["dataset_type"] = split

#         # 🧹 Delete old split before inserting new
#         articles_collection.delete_many({"dataset_type": split})

#         if articles:
#             result = articles_collection.insert_many(articles)
#             print(f"✅ Inserted {len(result.inserted_ids)} {split} articles into MongoDB (old ones replaced)")
#         else:
#             print(f"⚠️ No articles found in {file_path}")
#     else:
#         print(f"⚠️ File not found: {file_path}")

# ------------------ Main Pipeline ------------------ #
def run_pipeline():
    print("\n🚀 Starting full pipeline...\n")

    # 1. Scraper
    run_step("python scraper/scraper_requests_playwright.py", "Scraper")

    # 2. Preprocess
    run_step("python scraper/preprocess.py", "Preprocessing")

    # 3. Extractor
    run_step("python scraper/extractor_super_robust.py", "Extractor")

    # 4. Gold file generation
    print("📝 Generating testing_gold.json ...")
    extracted_path = "data/extracted_multilang/testing_articles.json"
    gold_path = "data/testing_gold.json"

    if os.path.exists(extracted_path):
        with open(extracted_path, "r", encoding="utf-8") as f:
            testing_articles = json.load(f)

        gold_data = []
        for article in testing_articles:
            gold_data.append({
                "url": article.get("url"),
                "language": article.get("language"),
                "headline": article.get("title", ""),
                "body": article.get("body", "")
            })

        os.makedirs(os.path.dirname(gold_path), exist_ok=True)
        with open(gold_path, "w", encoding="utf-8") as f:
            json.dump(gold_data, f, indent=2, ensure_ascii=False)

        print(f"✅ {gold_path} created.\n")
    else:
        print(f"⚠️ Extracted testing file not found: {extracted_path}")

    # 5. Evaluation
    run_step("python scraper/evaluate_extractor.py", "Evaluation")

    # 6. Insert into MongoDB
    # insert_articles_to_mongo("data/extracted_multilang/training_articles.json", "training")
    # insert_articles_to_mongo("data/extracted_multilang/testing_articles.json", "testing")

    print("🎉 Pipeline finished successfully!\n")

# ------------------ Scheduler ------------------ #
def schedule_pipeline():
    # Run once immediately
    run_pipeline()

    # Schedule daily at 2 AM
    schedule.every().day.at("02:00").do(run_pipeline)
    print("📅 Pipeline scheduled to run daily at 2:00 AM.")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_pipeline()
