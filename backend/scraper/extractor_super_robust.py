import json, os, re, unicodedata
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory, LangDetectException

PREPROCESSED_DIR = "data/preprocessed"
OUTPUT_DIR = "data/extracted_multilang"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SHORT_ARTICLE_THRESHOLD = 20
DetectorFactory.seed = 0

def clean_text(text):
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", text).strip()

def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def extract_title(soup):
    candidates = [t.get_text(strip=True) for t in soup.find_all(['h1','h2']) if t.get_text(strip=True)]
    if candidates: return max(candidates, key=len)
    title_tag = soup.find('title')
    if title_tag and title_tag.get_text(strip=True): return title_tag.get_text(strip=True)
    meta_desc = soup.find('meta', {'name':'description'}) or soup.find('meta', {'property':'og:title'})
    if meta_desc and meta_desc.get('content'): return meta_desc.get('content').strip()
    return ""

def extract_body(soup):
    candidates = []
    for article_tag in soup.find_all('article'):
        text = article_tag.get_text(separator=' ', strip=True)
        if text: candidates.append(text)
    paragraphs = [p.get_text(separator=' ', strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
    candidates.extend(paragraphs)
    divs = [div.get_text(separator=' ', strip=True) for div in soup.find_all('div') if div.get_text(strip=True)]
    candidates.extend(divs)
    if not candidates:
        meta_desc = soup.find('meta', {'name':'description'}) or soup.find('meta', {'property':'og:description'})
        if meta_desc and meta_desc.get('content'): return meta_desc.get('content').strip()
        return ""
    return max(candidates, key=len)

def extract_article(article):
    html = article.get("html","")
    if not html.strip(): return None
    soup = BeautifulSoup(html,'html.parser')
    title = clean_text(extract_title(soup))
    body = clean_text(extract_body(soup))
    if not title or not body or len(body.split())<SHORT_ARTICLE_THRESHOLD: return None
    return {
        "url": article.get("url"),
        "source": article.get("source"),
        "type": article.get("type","unknown"),
        "language": detect_language(body),
        "title": title,
        "body": body
    }

def extract_json(input_path, output_path):
    with open(input_path,"r",encoding="utf-8") as f: articles = json.load(f)
    extracted = [a for a in (extract_article(a) for a in articles) if a]
    with open(output_path,"w",encoding="utf-8") as f: json.dump(extracted,f,ensure_ascii=False,indent=2)
    print(f"✅ Extracted {len(extracted)} articles -> {output_path}")

if __name__=="__main__":
    extract_json(os.path.join(PREPROCESSED_DIR,"training_articles.json"), os.path.join(OUTPUT_DIR,"training_articles.json"))
    extract_json(os.path.join(PREPROCESSED_DIR,"testing_articles.json"), os.path.join(OUTPUT_DIR,"testing_articles.json"))
