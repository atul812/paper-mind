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

    # Adjust UMAP parameters based on dataset size
    n_neighbors = max(3, min(15, len(abstracts) - 1))
    n_components = max(2, min(5, len(abstracts) - 1))
    
    umap_model = UMAP(
        n_neighbors=n_neighbors,
        n_components=n_components,
        min_dist=0.0,
        metric="cosine",
        random_state=42,
    )

    # Adjust HDBSCAN parameters based on dataset size
    min_cluster_size = max(2, min(10, len(abstracts) // 2))
    
    hdbscan_model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        metric="euclidean",
        prediction_data=True,
    )

    # Adjust min_topic_size based on dataset size
    min_topic_size = max(2, min(10, len(abstracts) // 3))
    
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        min_topic_size=min_topic_size,
        verbose=True,
    )

    topics, probs = topic_model.fit_transform(abstracts)

    # Ensure papers list length matches topics list
    if len(papers) != len(topics):
        raise ValueError(
            f"Papers list length ({len(papers)}) does not match topics length ({len(topics)})"
        )
    
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