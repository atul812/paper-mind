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
        window_weeks=1  # 1 week windows for granular temporal resolution
    )
    

    papers,topic_map=run_topic_modeling(
        papers
    )

    tfidf_matrix=compute_tfidf_scores(
        papers
    )

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
        horizon_windows=4  # Forecast 4 weeks ahead (1 month)
    )

    top_accelerating=get_top_accelerating(
        velocity,
        topic_map,
        n=5
    )

    serializable_papers=[]
    for p in papers:
        published_date = p.get("published_date")
        serializable_papers.append({
            **p,
            "published_date":
                published_date.isoformat()
                if hasattr(published_date, "isoformat")
                else published_date
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