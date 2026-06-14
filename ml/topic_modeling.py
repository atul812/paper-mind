from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
import pandas as pd

EMBEDDING_MODEL = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

RESEARCH_STOP_WORDS = {
    "et", "al", "figure", "method", "paper", "result",
    "approach", "study", "dataset", "model", "learning",
}


def run_topic_modeling(papers):

    abstracts = [p["abstract"] for p in papers]

    # Adjust UMAP parameters based on dataset size
    n_neighbors = max(3, min(15, len(abstracts) - 1))
    n_components = max(2, min(5, len(abstracts) - 1))
    
    umap_model = UMAP(
        n_neighbors=n_neighbors,
        n_components=n_components,
        min_dist=0.0,
        metric="cosine",
        random_state=42,
        init="random",
    )

    # Adjust HDBSCAN parameters based on dataset size
    min_cluster_size = max(2, min(15, max(2, len(abstracts) // 10)))
    
    hdbscan_model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=1,
        metric="euclidean",
        prediction_data=True,
    )

    # Adjust min_topic_size based on dataset size
    min_topic_size = max(2, min(15, max(2, len(abstracts) // 10)))

    # Use a research-aware vectorizer to remove stop words and capture common n-grams
    research_stop_words = {
        "et", "al", "figure", "method", "paper", "result",
        "approach", "study", "dataset", "model", "learning",
    }
    vectorizer_model = CountVectorizer(
        stop_words=list(set(ENGLISH_STOP_WORDS).union(RESEARCH_STOP_WORDS)),
        ngram_range=(1, 2),
        min_df=1,
        max_df=1.0,
        max_features=500,
    )
    
    topic_model = BERTopic(
        embedding_model=EMBEDDING_MODEL,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        min_topic_size=min_topic_size,
        verbose=False,
    )

    try:
        topics, probs = topic_model.fit_transform(abstracts)
    except Exception:
        # BERTopic may fail on very small or noisy inputs.
        # Fall back to a single general topic so the backend remains stable.
        for idx in range(len(papers)):
            papers[idx]["topic_id"] = 0
        return papers, {0: ["general"]}

    # Ensure papers list length matches topics list
    if len(papers) != len(topics):
        raise ValueError(
            f"Papers list length ({len(papers)}) does not match topics length ({len(topics)})"
        )
    
    for idx, topic_id in enumerate(topics):
        papers[idx]["topic_id"] = int(topic_id)

    research_stop_words = {
        "et", "al", "figure", "method", "paper", "result",
        "approach", "study", "dataset", "model", "learning",
    }
    topic_labels = {}

    for topic_id in topic_model.get_topics():

        if topic_id == -1:
            continue

        all_words = topic_model.get_topic(topic_id, full=False)
        
        keywords = [
            word for word, _ in all_words
            if word.lower() not in ENGLISH_STOP_WORDS
            and word.lower() not in research_stop_words
        ]
        
        if keywords:
            keywords = keywords[:5]
        else:
            keywords = [word for word, _ in all_words[:5]]

        topic_labels[topic_id] = keywords

    return papers, topic_labels