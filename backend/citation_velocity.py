from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd


def compute_citation_velocity(papers):
    rows=[]
    grouped={}

    # Handle both list and DataFrame inputs
    if isinstance(papers, pd.DataFrame):
        # Convert DataFrame to list of dicts
        papers_list = papers.to_dict('records')
    else:
        papers_list = papers
    
    for p in papers_list:

        if p["topic_id"]==-1:
            continue
        key=(p["topic_id"],p["window"])
        grouped[key]=grouped.get(key,0)+p["citation_count"]

    for (topic,window),citations in grouped.items():

        rows.append({
            "topic_id":topic,
            "window":window,
            "citations":citations
        })

    df=pd.DataFrame(rows)
    results=[]

    for topic in df.topic_id.unique():
        topic_id = int(topic)
        topic_df=df[
            df.topic_id==topic
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