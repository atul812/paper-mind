from backend.momentum import compute_momentum

def test_momentum():

    publication_velocity=[
        {
            "topic_id":0,
            "velocity":1.0
        }
    ]

    citation_velocity=[
        {
            "topic_id":0,
            "citation_velocity":2.0
        }
    ]

    result=compute_momentum(
        publication_velocity,
        citation_velocity
    )

    assert len(result)==1
    assert result[0]["topic_id"]==0
    assert "momentum" in result[0]
    assert "momentum_trend" in result[0]