import pandas as pd
from backend.citation_velocity import compute_citation_velocity

def test_citation_velocity():

    df=pd.DataFrame([

        {
            "topic_id":0,
            "window":"2024_W0",
            "citation_count":10
        },

        {

            "topic_id":0,
            "window":"2024_W1",
            "citation_count":20

        },

        {
            "topic_id":0,
            "window":"2025_W0",
            "citation_count":30
        }
    ])

    result=compute_citation_velocity(df)

    assert len(result)==1
    assert result[0]["topic_id"]==0
    assert "citation_velocity" in result[0]