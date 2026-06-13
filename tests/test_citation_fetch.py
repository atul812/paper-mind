from backend.citation_fetch import enrich_with_citations

def test_citation_fetch():

    papers=[

        {

            "id":"2301.00001",

            "title":"test",

            "abstract":"test",

            "authors":[],

            "published_date":"2024-01-01",

            "window":"2024_W0",

            "topic_id":0

        }

    ]


    result=enrich_with_citations(papers)


    assert "citation_count" in result[0]

    assert "influential_citation_count" in result[0]

    assert isinstance(result[0]["citation_count"],int)