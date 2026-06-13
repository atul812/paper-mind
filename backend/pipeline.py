from backend.data_fetch import fetch_papers
from backend.citation_fetch import enrich_with_citations
from backend.time_windows import compute_time_windows
from backend.tfidf_scoring import compute_tfidf_scores
from backend.velocity import compute_velocity
from backend.citation_velocity import compute_citation_velocity
from backend.momentum import compute_momentum
from backend.forecasting import forecast_topics
from backend.trend_analysis import get_top_accelerating

try:
    from ml.topic_modeling import run_topic_modeling
except ImportError:
    run_topic_modeling=None

def run_pipeline(query):

    if run_topic_modeling is None:
        raise NotImplementedError(
            "run_topic_modeling() is not implemented yet."
        )

    papers=fetch_papers(query)
    papers=enrich_with_citations(papers)
    papers=compute_time_windows(
        papers,
        window_months=6
    )
    print("\nWINDOWS FOUND:")
    print(sorted(list(set(p["window"] for p in papers))))

    print("\nEARLIEST DATE:")
    print(min(p["published_date"] for p in papers))

    print("\nLATEST DATE:")
    print(max(p["published_date"] for p in papers))

    papers,topic_map=run_topic_modeling(
        papers
    )
    print("\nTOPIC IDS:")
    print(set(p["topic_id"] for p in papers))

    print("\nTOPIC MAP:")
    print(topic_map)

    tfidf_matrix=compute_tfidf_scores(
        papers
    )

    print("\nTFIDF MATRIX")
    print(tfidf_matrix.head())

    print("\nTFIDF COLUMNS")
    print(tfidf_matrix.columns)

    print("\nWINDOWS")
    print(tfidf_matrix["window"].unique())
    velocity=compute_velocity(
        tfidf_matrix
    )

    citation_velocity=compute_citation_velocity(
        papers
    )

    momentum=compute_momentum(
        velocity,
        citation_velocity
    )

    forecast=forecast_topics(
        tfidf_matrix,
        horizon_months=12
    )

    top_accelerating=get_top_accelerating(
        velocity,
        topic_map,
        n=5
    )

    serializable_papers=[]
    for p in papers:
        serializable_papers.append({
            **p,
            "published_date":p["published_date"].isoformat()
        })


    return {
        "papers":serializable_papers,
        "topic_map":topic_map,
        "tfidf_matrix":tfidf_matrix.to_dict(
            orient="records"
        ),
        "velocity":velocity,
        "citation_velocity":citation_velocity,
        "momentum":momentum,
        "forecast":forecast,
        "top_accelerating":top_accelerating

    }