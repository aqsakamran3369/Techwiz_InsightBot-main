# ---------------- Required Libraries ----------------
import pandas as pd
import re
from collections import Counter
import nltk
import numpy as np
nltk.download('stopwords')
from nltk.corpus import stopwords

# ---------------- Load Existing Dataset ----------------
df = pd.read_json('data/all_articles.json')  # ya pd.read_csv('data/all_articles.csv')

# ---------------- Combine Title & Body ----------------
df['text'] = df['title'].fillna('') + ' ' + df['body'].fillna('')

# ---------------- Text Cleaning ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # keep only alphabets & spaces
    return text

df['clean_text'] = df['text'].apply(clean_text)

# ---------------- Tokenization & Stopwords Removal ----------------
stop_words = set(stopwords.words('english'))

def tokenize(text):
    return [word for word in text.split() if word not in stop_words and len(word) > 2]

df['tokens'] = df['clean_text'].apply(tokenize)

# ---------------- Explode tokens for language-wise counting ----------------
df_exploded = df.explode('tokens')
df_exploded = df_exploded[['tokens','lang']].rename(columns={'tokens':'Word','lang':'Language'})

# ---------------- Word Frequency Count (Language-wise) ----------------
df_exploded_grouped = df_exploded.groupby(['Word','Language']).size().reset_index(name='Count')

# ---------------- Top 200 Words per Language ----------------
df_top = df_exploded_grouped.groupby('Language').apply(lambda x: x.nlargest(200, 'Count')).reset_index(drop=True)

# ---------------- Log Scaling for Tableau ----------------
df_top['Count_Log'] = df_top['Count'].apply(lambda x: np.log1p(x))  # log(1 + count)

# ---------------- Save CSV for Tableau ----------------
df_top.to_csv('tableau/wordcloud_data_lang_top200.csv', index=False)

print("✅ Top 200 words per language CSV with log-scaled counts ready for Tableau!")
