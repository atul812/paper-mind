from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def compute_tfidf_scores(papers):

    docs = []
    labels = []
    grouped = defaultdict(str)

    for p in papers:
        topic_id = p.get("topic_id", -1)
        if topic_id == -1:
            continue

        window = p.get("window")
        abstract = p.get("abstract", "")
        if window is None or abstract is None:
            continue

        key = (
            topic_id,
            window
        )

        grouped[key] += (" " + abstract)

    for key, text in grouped.items():
        labels.append(key)
        docs.append(text)

    if not docs:
        return pd.DataFrame(
            columns=[
                "topic_id",
                "window",
                "score"
            ]

        )
    tfidf = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    X = tfidf.fit_transform(docs)

    scores = X.sum(axis=1)
    scores = scores.A1
    rows = []

    for i, (topic, window) in enumerate(labels):

        rows.append({
            "topic_id": int(topic),
            "window": window,
            "score": float(scores[i])
        })

    return pd.DataFrame(rows)