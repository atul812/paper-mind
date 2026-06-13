import requests
import feedparser
from datetime import datetime

BASE_URL = "https://export.arxiv.org/api/query"


def fetch_papers(query, max_results=150):

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"

    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()
    feed = feedparser.parse(response.text)
    papers = []

    for entry in feed.entries:

        paper = {

            "id":
            entry.id.split("/")[-1],

            "title":
            entry.title.replace(
                "\n",
                " "
            ).strip(),

            "abstract":
            entry.summary.replace(
                "\n",
                " "
            ).strip(),

            "authors":[author.name for author in entry.authors],

            "published_date":
            datetime.strptime(entry.published,"%Y-%m-%dT%H:%M:%SZ"),
            "topic_id":-1,
            "citation_count":0,
            "influential_citation_count":0,
            "window":None

        }

        papers.append(paper)

    return papers