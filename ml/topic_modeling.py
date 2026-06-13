from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
import pandas as pd


def run_topic_modeling(papers):

    abstracts = [p["abstract"] for p in papers]

    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    umap_model = UMAP(
        n_neighbors=15,
        n_components=5,
        min_dist=0.0,
        metric="cosine",
        random_state=42,
    )

    hdbscan_model = HDBSCAN(
        min_cluster_size=10,
        metric="euclidean",
        prediction_data=True,
    )

    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        min_topic_size=10,
        verbose=True,
    )

    topics, probs = topic_model.fit_transform(abstracts)

    for idx, topic_id in enumerate(topics):
        papers[idx]["topic_id"] = int(topic_id)

    topic_labels = {}

    for topic_id in topic_model.get_topics():

        if topic_id == -1:
            continue

        words = topic_model.get_topic(topic_id)

        topic_labels[topic_id] = [
            word for word, _ in words[:5]
        ]

    return papers, topic_labels