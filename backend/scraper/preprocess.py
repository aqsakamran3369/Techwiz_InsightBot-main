import json, os, re, unicodedata
from bs4 import BeautifulSoup

RAW_TRAINING_PATH = "data/training_articles.json"
RAW_TESTING_PATH = "data/testing_articles.json"
PREPROCESSED_DIR = "data/preprocessed"
os.makedirs(PREPROCESSED_DIR, exist_ok=True)

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(['script','style','header','footer','nav','aside','form','iframe']):
        tag.extract()
    return soup.get_text(separator=" ", strip=True)

def normalize_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_json(input_path, output_path, min_words=10):
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    preprocessed = []
    for art in articles:
        html = art.get("html", "")
        clean_text = normalize_text(clean_html(html)) if html.strip() else ""
        preprocessed.append({
            "url": art.get("url"),
            "source": art.get("source"),
            "html": html,
            "clean_text": clean_text,
            "type": art.get("type", "unknown"),
            "short_article": len(clean_text.split()) < min_words  # mark short ones
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(preprocessed, f, ensure_ascii=False, indent=2)

# Run preprocessing
preprocess_json(RAW_TRAINING_PATH, os.path.join(PREPROCESSED_DIR, "training_articles.json"))
preprocess_json(RAW_TESTING_PATH, os.path.join(PREPROCESSED_DIR, "testing_articles.json"))
