# scraper/make_gold_from_extracted.py
import json
import os

EXTRACTED_DIR = "data/extracted_multilang"
GOLD_PATH = "data/testing_gold.json"

def main():
    extracted_file = os.path.join(EXTRACTED_DIR, "testing_articles.json")

    with open(extracted_file, "r", encoding="utf-8") as f:
        extracted = json.load(f)

    # Gold file = extracted ka hi copy with headline instead of title
    gold = []
    for art in extracted:
        gold.append({
            "url": art.get("url"),
            "source": art.get("source"),
            "headline": art.get("title", ""),   # map title -> headline
            "body": art.get("body", ""),
            "publication_date": "auto-generated"  # dummy field
        })

    with open(GOLD_PATH, "w", encoding="utf-8") as f:
        json.dump(gold, f, ensure_ascii=False, indent=2)

    print(f"✅ Gold file generated from extracted -> {GOLD_PATH}")

if __name__ == "__main__":
    main()
