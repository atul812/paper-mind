from ml.topic_modeling import run_topic_modeling

def test_run_topic_modeling():
    papers = [
        {
            "title": "Federated Learning for Healthcare",
            "abstract": """
            Federated learning enables privacy-preserving
            medical diagnosis across hospitals.
            """
        },
        {
            "title": "Secure Aggregation",
            "abstract": """
            Secure aggregation improves privacy and security
            in federated learning systems.
            """
        },
        {
            "title": "Communication Efficient FL",
            "abstract": """
            Communication compression techniques reduce
            bandwidth usage in federated learning.
            """
        },
        {
            "title": "Edge AI",
            "abstract": """
            Edge devices can train federated learning
            models locally while preserving privacy.
            """
        }
    ]

    tagged_papers, topic_labels = run_topic_modeling(papers)

    assert len(tagged_papers) == len(papers)

    for paper in tagged_papers:
        assert "topic_id" in paper

    assert isinstance(topic_labels, dict)

    print("\nGenerated Topics:")
    print(topic_labels)

    print("\nTagged Papers:")
    for paper in tagged_papers:
        print(
            f"{paper['title']} -> Topic {paper['topic_id']}"
        )

if __name__ == "__main__":
    test_run_topic_modeling()