import subprocess
import schedule
import time
import os
import json
from pymongo import MongoClient

EXTRACTED_DIR = "data/extracted_multilang"
MONGO_URI = "mongodb+srv://thewebwiz23:TheWebWiz2988@cluster0.8edmm.mongodb.net/insightbot_db?retryWrites=true&w=majority"

def run_step(cmd, desc):
    print(f"\n🚀 {desc}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"❌ Step failed: {desc}")
        exit(1)

def generate_gold_file():
    extracted_file = os.path.join(EXTRACTED_DIR, "testing_articles.json")
    GOLD_PATH = "data/testing_gold.json"

    if not os.path.exists(extracted_file):
        print(f"⚠️ Extracted testing file not found: {extracted_file}")
        return

    with open(extracted_file, "r", encoding="utf-8") as f:
        extracted = json.load(f)

    gold = []
    for art in extracted:
        gold.append({
            "url": art.get("url"),
            "source": art.get("source"),
            "headline": art.get("title", ""),
            "body": art.get("body", ""),
            "publication_date": "auto-generated"
        })

    os.makedirs(os.path.dirname(GOLD_PATH), exist_ok=True)
    with open(GOLD_PATH, "w", encoding="utf-8") as f:
        json.dump(gold, f, ensure_ascii=False, indent=2)

    print(f"✅ Gold file generated -> {GOLD_PATH}")

def insert_articles_to_db():
    client = MongoClient(MONGO_URI)
    db = client.insightbot_db
    articles_collection = db.articles

    for split in ["training", "testing"]:
        file_path = os.path.join(EXTRACTED_DIR, f"{split}_articles.json")
        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            articles = json.load(f)

        for art in articles:
            art["dataset_type"] = split
            art.pop("_id", None)

        if articles:
            result = articles_collection.insert_many(articles)
            print(f"✅ Inserted {len(result.inserted_ids)} {split} articles into MongoDB")
        else:
            print(f"⚠️ No {split} articles to insert.")

def run_pipeline():
    run_step("python scraper/scraper_requests_playwright.py", "Scraping")
    run_step("python scraper/preprocess.py", "Preprocessing")
    run_step("python scraper/extractor_super_robust.py", "Extracting")
    run_step("python scraper/make_gold_from_extracted.py", "Generating Gold File")
    run_step("python scraper/evaluate_extractor.py", "Evaluating")
    insert_articles_to_db()
    print("\n🎉 Pipeline finished!")

if __name__ == "__main__":
    # Run immediately once
    run_pipeline()

    # Schedule the pipeline to run every day at 2 AM
    schedule.every().day.at("02:00").do(run_pipeline)

    print("⏱️ Scheduler started: Pipeline will run daily at 02:00 AM")
    while True:
        schedule.run_pending()
        time.sleep(60)
