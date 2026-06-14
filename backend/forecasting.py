from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_topics(tfidf_matrix, horizon_windows=4, min_points_for_forecast=4):
    """
    Forecast topic TFIDF scores into the future.
    
    Args:
        tfidf_matrix: DataFrame with columns [topic_id, window, score]
        horizon_windows: Number of windows to forecast ahead
        min_points_for_forecast: Minimum data points required for a useful forecast
    """
    forecasts=[]
    
    # Handle empty DataFrame
    if tfidf_matrix.empty or "topic_id" not in tfidf_matrix.columns:
        return []
    
    for topic in tfidf_matrix["topic_id"].unique():
        topic_id = int(topic)

        df = tfidf_matrix[tfidf_matrix["topic_id"] == topic].sort_values("window")
        y = df["score"].values

        if len(y) < min_points_for_forecast:
            pred = float(y[-1]) if len(y) > 0 else 0.0
            predicted_trend = "→"
        else:
            x = np.arange(len(y)).reshape(-1, 1)

            model = LinearRegression()
            model.fit(x, y)
            future = np.array([[len(y) + horizon_windows - 1]])
            pred = float(model.predict(future)[0])

            if pred > y[-1]:
                predicted_trend = "↑"
            elif pred < y[-1]:
                predicted_trend = "↓"
            else:
                predicted_trend = "→"

        forecasts.append({
            "topic_id": topic_id,
            "current_score": float(y[-1]) if len(y) > 0 else 0.0,
            "predicted_score": float(pred),
            "predicted_trend": predicted_trend
        })
    return forecasts