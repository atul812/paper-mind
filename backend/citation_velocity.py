from sklearn.linear_model import LinearRegression
from datetime import datetime
import numpy as np
import pandas as pd


def compute_citation_velocity(papers, min_age_days=0):
    rows=[]
    grouped={}

    # Handle both list and DataFrame inputs
    if isinstance(papers, pd.DataFrame):
        # Convert DataFrame to list of dicts
        papers_list = papers.to_dict('records')
    else:
        papers_list = papers
    
    now = datetime.now()
    def _safe_number(value):
        if value is None:
            return 0.0
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    for p in papers_list:

        if p.get("topic_id") == -1:
            continue

        published_date = p.get("published_date")
        if published_date is not None and min_age_days > 0:
            age_days = (now - published_date).days
            if age_days < min_age_days:
                continue

        citation_weight = (
            _safe_number(p.get("citation_count")) * 0.4 +
            _safe_number(p.get("influential_citation_count")) * 0.6
        )

        topic_id = p.get("topic_id")
        window = p.get("window")
        if topic_id is None or topic_id == -1 or window is None:
            continue

        key = (topic_id, window)
        grouped[key] = grouped.get(key, 0) + citation_weight

    for (topic,window),citations in grouped.items():

        rows.append({
            "topic_id":topic,
            "window":window,
            "citations":citations
        })

    if not rows:
        return []

    df=pd.DataFrame(rows)
    if df.empty or "topic_id" not in df.columns:
        return []

    results=[]

    for topic in df["topic_id"].unique():
        topic_id = int(topic)
        topic_df = df[
            df["topic_id"] == topic
        ].sort_values("window")

        y=topic_df["citations"].values
        if len(y)<2:
            slope = 0.0
            trend = "→"
        else:
            x=np.arange(len(y)).reshape(-1,1)

            model=LinearRegression().fit(x,y)
            slope=model.coef_[0]

            if slope>0.1:
                trend="↑"

            elif slope<-0.1:
                trend="↓"

            else:
                trend="→"

        results.append({
            "topic_id": topic_id,
            "citation_velocity": float(slope),
            "citation_trend": trend
        })

    return results