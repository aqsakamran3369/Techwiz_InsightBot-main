import pandas as pd
import json
import os
import asyncio
import requests
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

RAW_TRAINING_PATH = "data/training_articles.json"
RAW_TESTING_PATH = "data/testing_articles.json"
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def scrape_requests(url, timeout=15):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            return resp.text
    except:
        return ""
    return ""

async def scrape_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0")
        page = await context.new_page()
        try:
            await page.goto(url, timeout=120000)
            await page.wait_for_load_state("networkidle", timeout=120000)
            html = await page.content()
        except:
            html = ""
        await browser.close()
    return html

async def scrape_sites(df, type_):
    articles = []
    for _, row in df.iterrows():
        url = row["url"]
        html = scrape_requests(url)
        if not html:
            html = await scrape_playwright(url)
        articles.append({
            "url": url,
            "source": url.split("//")[-1].split("/")[0],
            "html": html,
            "type": type_
        })
    return articles

async def main():
    df = pd.read_csv("data/websites.csv")
    training_df = df[df["type"] == "training"]
    testing_df = df[df["type"] == "testing"]

    training_articles = await scrape_sites(training_df, "training")
    with open(RAW_TRAINING_PATH, "w", encoding="utf-8") as f:
        json.dump(training_articles, f, ensure_ascii=False, indent=2)

    testing_articles = await scrape_sites(testing_df, "testing")
    with open(RAW_TESTING_PATH, "w", encoding="utf-8") as f:
        json.dump(testing_articles, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
