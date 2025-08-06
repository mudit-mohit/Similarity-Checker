import re
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

def calculate_similarity_score(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([clean_text(text1), clean_text(text2)])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(score * 100, 2)

def highlight_differences(text1, text2):
    differ = difflib.Differ()
    diff = list(differ.compare(text1.split(), text2.split()))

    highlighted_text1 = ""
    highlighted_text2 = ""

    for word in diff:
        if word.startswith(" "):
            word_text = word[2:] + " "
            highlighted_text1 += word_text
            highlighted_text2 += word_text
        elif word.startswith("- "):
            highlighted_text1 += f"[{word[2:]}] "
        elif word.startswith("+ "):
            highlighted_text2 += f"[{word[2:]}]"

    return highlighted_text1.strip(), highlighted_text2.strip()