import requests
import time

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/"
_cache = {}

def get_citation_data(arxiv_id):
    if arxiv_id in _cache:
        return _cache[arxiv_id]

    paper_id = f"ARXIV:{arxiv_id}"
    fields = (
        "citationCount",
        "influentialCitationCount",
        "title"
    )

    url = BASE_URL + paper_id
    try:
        response = requests.get(
            url,
            params={
                "fields": fields
            },
            timeout=20
        )

        if response.status_code != 200:
            result = {
                "citation_count": 0,
                "influential_citation_count": 0
            }
            _cache[arxiv_id] = result
            return result
        data = response.json()

        result = {
           "citation_count":data.get("citationCount",0),
            "influential_citation_count":
            data.get(
                "influentialCitationCount",0
            )
        }
        _cache[arxiv_id] = result
        time.sleep(0.05)
        return result

    except Exception:

        result = {
            "citation_count": 0,
            "influential_citation_count": 0

        }
        _cache[arxiv_id] = result
        return result

def enrich_with_citations(papers):
    enriched = []
    for paper in papers:
        arxiv_id = paper["id"]
        citation_data = get_citation_data(
            arxiv_id
        )
        paper["citation_count"] = (
            citation_data[
                "citation_count"
            ]
        )
        paper["influential_citation_count"] = (
            citation_data[
                "influential_citation_count"
            ]
        )
        enriched.append(paper)

    return enriched