#!/usr/bin/env python3
"""
Debug script to check Semantic Scholar API responses
"""
import requests
import time

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/"

test_arxiv_ids = [
    ("2106.14881", "GPT-3 or similar"),
    ("1706.03762", "Attention is All You Need"),
    ("1512.03385", "ResNet"),
]

print("=" * 70)
print("SEMANTIC SCHOLAR API DEBUG - Testing ARXIV: lookup format")
print("=" * 70)
print()

for arxiv_id, description in test_arxiv_ids:
    paper_id = f"ARXIV:{arxiv_id}"
    fields = ("citationCount", "influentialCitationCount", "title")
    url = BASE_URL + paper_id
    
    print(f"Paper: {description}")
    print(f"  ArXiv ID: {arxiv_id}")
    print(f"  Querying: {url}")
    
    try:
        response = requests.get(
            url,
            params={"fields": ",".join(fields)},
            timeout=5
        )
        
        print(f"  HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Response: {data}")
            print(f"  Citation Count: {data.get('citationCount', 'N/A')}")
            print(f"  Influential: {data.get('influentialCitationCount', 'N/A')}")
        else:
            print(f"  Response text: {response.text[:200]}")
            
    except Exception as e:
        print(f"  ERROR: {e}")
    
    print()
    time.sleep(1)  # Rate limiting

print("=" * 70)
print("NOTE: If status codes are not 200, the ARXIV: lookup format may be")
print("incorrect or Semantic Scholar may have changed their API.")
print("=" * 70)
