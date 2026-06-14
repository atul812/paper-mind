import requests
import time
import re

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/"
_cache = {}
MAX_CITATION_PAPERS = 12

def get_citation_data(arxiv_id):
    # Strip version suffix (e.g., '2106.12345v2' -> '2106.12345')
    # using regex: match the pattern XXXX.XXXXX (4 digits, dot, 5 digits)
    # Semantic Scholar's ARXIV: lookup doesn't resolve versioned IDs
    match = re.match(r'^(\d{4}\.\d{4,5})', arxiv_id)
    arxiv_id_clean = match.group(1) if match else arxiv_id
    
    # Check cache using the cleaned ID (all variants map to the same cache entry)
    if arxiv_id_clean in _cache:
        return _cache[arxiv_id_clean]

    paper_id = f"ARXIV:{arxiv_id_clean}"
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
            timeout=12
        )

        if response.status_code != 200:
            result = {
                "citation_count": 0,
                "influential_citation_count": 0
            }
            _cache[arxiv_id_clean] = result
            return result
        data = response.json()

        result = {
            "citation_count": data.get("citationCount", None),
            "influential_citation_count": data.get("influentialCitationCount", None),
        }
        _cache[arxiv_id_clean] = result
        return result

    except Exception:

        result = {
            "citation_count": 0,
            "influential_citation_count": 0

        }
        _cache[arxiv_id_clean] = result
        return result

def enrich_with_citations(papers):
    enriched = []
    for index, paper in enumerate(papers):
        if index >= MAX_CITATION_PAPERS:
            enriched.append(paper)
            continue

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