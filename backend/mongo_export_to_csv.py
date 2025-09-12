import json
import pandas as pd

# ---------------- Paths ----------------
json_path = "data/all_articles.json"          # tumhara JSON file
csv_path = "tableau/articles_export.csv"     # destination CSV file

# ---------------- Load JSON ----------------
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---------------- Convert to DataFrame ----------------
df = pd.DataFrame(data)

# ---------------- Optional: Handle _id if present ----------------
if '_id' in df.columns:
    df['_id'] = df['_id'].astype(str)  # ya del df['_id']

# ---------------- Export to CSV ----------------
df.to_csv(csv_path, index=False, encoding='utf-8-sig')  # utf-8-sig for multilingual support

print(f"✅ CSV successfully created at {csv_path}")
