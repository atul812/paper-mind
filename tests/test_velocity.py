import pandas as pd
from backend.velocity import compute_velocity

def test_compute_velocity():
    df=pd.DataFrame([

        {
            "topic_id":0,
            "window":"2024_W0",
            "score":1.0
        },

        {
            "topic_id":0,
            "window":"2024_W1",
            "score":2.0
        },

        {
            "topic_id":0,
            "window":"2025_W0",
            "score":3.0
        }

    ])

    result=compute_velocity(
        df
    )

    assert len(result)==1
    assert result[0]["topic_id"]==0
    assert result[0]["trend"]=="↑"