from sklearn.linear_model import LinearRegression

import numpy as np


def compute_velocity(tfidf_matrix):

    results = []
    for topic in tfidf_matrix.topic_id.unique():

        df = tfidf_matrix[
            tfidf_matrix.topic_id == topic ].sort_values("window")
        y = df["score"].values
        if len(y) < 2:
            continue

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
            "topic_id": topic,
            "velocity": float(slope),
            "trend": trend
        })
    return results