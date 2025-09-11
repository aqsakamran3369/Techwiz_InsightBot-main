import json, os
from fuzzywuzzy import fuzz
from difflib import SequenceMatcher

# Paths
OUTPUT_DIR = "data/extracted_multilang"
GOLD_PATH = "data/testing_gold.json"

def jaccard(a, b):
    set1, set2 = set(a.lower().split()), set(b.lower().split())
    return len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0.0

def evaluate(extracted_path, gold_path):
    with open(extracted_path, "r", encoding="utf-8") as f:
        extracted = {art["url"]: art for art in json.load(f)}
    with open(gold_path, "r", encoding="utf-8") as f:
        gold = {art["url"]: art for art in json.load(f)}

    urls = list(gold.keys())
    total, matched = 0, 0

    print("\n🔎 DEBUG COMPARISON\n" + "="*70)
    for url in urls:
        total += 1
        g = gold[url]
        e = extracted.get(url, {})

        gold_title = g.get("headline", "").strip()
        gold_body = g.get("body", "").strip()
        ext_title = e.get("title", "").strip()
        ext_body = e.get("body", "").strip()

        # Similarities
        title_j = jaccard(gold_title, ext_title)
        body_j = jaccard(gold_body, ext_body)
        title_f = fuzz.ratio(gold_title, ext_title) / 100
        body_f = fuzz.ratio(gold_body, ext_body) / 100

        # Match condition (adjustable threshold)
        if title_f > 0.7 and body_f > 0.7:
            matched += 1

        # Print debug info
        print(f"\nURL: {url}")
        print(f"Gold Title     : {gold_title}")
        print(f"Extracted Title: {ext_title}")
        print(f" → Title Jaccard={title_j:.2f}, Fuzzy={title_f:.2f}")

        print(f"Gold Body      : {gold_body[:120]}...")
        print(f"Extracted Body : {ext_body[:120]}...")
        print(f" → Body Jaccard={body_j:.2f}, Fuzzy={body_f:.2f}")
        print("-"*70)

    accuracy = matched / total if total > 0 else 0
    print(f"\n✅ Evaluation complete! Accuracy: {accuracy:.2%}")
    print(f"Total={total}, Matched={matched}, Failed={total-matched}")

if __name__ == "__main__":
    evaluate(os.path.join(OUTPUT_DIR, "testing_articles.json"), GOLD_PATH)
