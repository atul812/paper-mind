import pandas as pd
from backend.forecasting import forecast_topics

def test_forecast_topics():
    df=pd.DataFrame([

        {
            "topic_id":0,
            "window":"2024_W0",
            "score":1
        },

        {
            "topic_id":0,
            "window":"2024_W1",
            "score":2
        },

        {
            "topic_id":0,
            "window":"2025_W0",
            "score":3
        }

    ])

    result=forecast_topics(
        df
    )

    assert len(result)==1
    assert result[0]["topic_id"]==0
    assert "predicted_score" in result[0]