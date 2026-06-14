from sklearn.linear_model import LinearRegression

import numpy as np


def compute_velocity(tfidf_matrix):

    results = []
    
    # Handle empty DataFrame
    if tfidf_matrix.empty or "topic_id" not in tfidf_matrix.columns:
        return []
    
    for topic in tfidf_matrix["topic_id"].unique():
        topic_id = int(topic)

        df = tfidf_matrix[
            tfidf_matrix["topic_id"] == topic].sort_values("window")
        y = df["score"].values
        if len(y) < 2:
            slope = 0.0
            trend = "→"
        else:
            x = np.arange(
                len(y)
            ).reshape(-1,1)

            model = LinearRegression()
            model.fit(x,y)
            slope = model.coef_[0]

            if slope > 0.1:
                trend = "↑"

            elif slope < -0.1:
                trend = "↓"

            else:
                trend = "→"

        results.append({
            "topic_id": topic_id,
            "velocity": float(slope),
            "trend": trend
        })
    return results