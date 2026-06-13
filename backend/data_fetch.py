import requests
import feedparser
from datetime import datetime

BASE_URL = "http://export.arxiv.org/api/query"

def fetch_papers(query,max_results = 500):
    params = {"search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"}
    response = requests.get(BASE_URL,params=params)
    feed = feedparser.parse(response.text)

    papers = []
    for entry in feed.entries:
        paper = {
            "id":entry.id.split("/")[-1],
            "title": entry.title.replace("\n", " ").strip(),
            "abstract": entry.summary.replace("\n", " ").strip(),
            "authors": [author.name for author in entry.authors],

            "published_date":
                datetime.strptime(
                    entry.published,
                    "%Y-%m-%dT%H:%M:%SZ"
                ),

            "topic_id": None

        }

        papers.append(paper)
    return papers

        