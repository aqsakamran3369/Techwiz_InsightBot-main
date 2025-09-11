import json, os, re, unicodedata
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory, LangDetectException

DetectorFactory.seed = 0
PREPROCESSED_DIR = "data/preprocessed"
OUTPUT_DIR = "data/extracted_multilang"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", text).strip()

def detect_language(text):
    try: return detect(text)
    except LangDetectException: return "unknown"

def extract_title(soup):
    t = soup.find("h1") or soup.find("title")
    return t.get_text(strip=True) if t else ""

def extract_body(soup):
    p = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    return max(p, key=len) if p else ""

def extract_article(article):
    html = article.get("html", "")
    soup = BeautifulSoup(html, "html.parser") if html else None
    title = clean_text(extract_title(soup)) if soup else ""
    body = clean_text(extract_body(soup)) if soup else ""

    # Fallbacks
    if not title: title = "No Title"
    if not body: body = article.get("clean_text", "")[:100]  # take first 100 chars

    return {
        "url": article.get("url"),
        "source": article.get("source"),
        "title": title,
        "body": body,
        "language": detect_language(body),
        "short_article": len(body.split()) < 50
    }

def extract_json(input_path, output_path):
    with open(input_path,"r",encoding="utf-8") as f: arts=json.load(f)
    out = [extract_article(a) for a in arts]
    with open(output_path,"w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=2)

# Run extraction
extract_json(os.path.join(PREPROCESSED_DIR,"training_articles.json"),
             os.path.join(OUTPUT_DIR,"training_articles.json"))
extract_json(os.path.join(PREPROCESSED_DIR,"testing_articles.json"),
             os.path.join(OUTPUT_DIR,"testing_articles.json"))
