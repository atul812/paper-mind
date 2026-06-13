from backend.data_fetch import fetch_papers

def test_fetch_papers():

    papers=fetch_papers(
        "federated learning",
        max_results=5
    )
    assert len(papers)>0
    assert "title" in papers[0]
    assert "abstract" in papers[0]
    assert "published_date" in papers[0]