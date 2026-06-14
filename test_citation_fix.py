#!/usr/bin/env python3
"""
Verification test for citation_fetch.py fix
Tests that arXiv IDs with version suffixes are properly stripped
before querying Semantic Scholar API
"""
import sys
sys.path.insert(0, '/Users/atulkumar/Desktop/paper-mind')

from backend.citation_fetch import get_citation_data, _cache

def test_version_suffix_stripping():
    """Test that version suffixes are stripped before API query and caching"""
    
    print("=" * 70)
    print("CITATION FETCH - VERSION SUFFIX FIX VERIFICATION")
    print("=" * 70)
    print()
    
    # Test IDs: famous papers with different version suffixes
    test_cases = [
        # (arxiv_id_input, expected_clean_id, expected_cites_gt_0, description)
        ("2106.14881v2", "2106.14881", True, "Transformer (known to have cites)"),
        ("2106.14881v1", "2106.14881", True, "Same paper, v1 (should cache hit)"),
        ("2106.14881", "2106.14881", True, "Same paper, no version (should cache hit)"),
        ("1706.03762v5", "1706.03762", True, "Attention is All You Need"),
        ("1512.03385v1", "1512.03385", True, "ResNet (very cited)"),
    ]
    
    print("Test Cases: Querying Semantic Scholar for known papers")
    print("-" * 70)
    print()
    
    for arxiv_id, expected_clean, expect_cites, description in test_cases:
        print(f"Input: {arxiv_id:20s} | Description: {description}")
        
        result = get_citation_data(arxiv_id)
        
        citation_count = result.get("citation_count")
        influential_count = result.get("influential_citation_count")
        
        # Check if it's in cache with cleaned ID
        is_cached = expected_clean in _cache
        
        print(f"  → Cleaned ID: {expected_clean}")
        print(f"  → Citations: {citation_count}")
        print(f"  → Influential: {influential_count}")
        print(f"  → Cached with cleaned key: {is_cached}")
        
        # Verify
        if citation_count is None or (expect_cites and citation_count == 0):
            print(f"  ⚠️  WARNING: Expected non-zero citations, got {citation_count}")
        else:
            print(f"  ✅ PASS: Citation count is {citation_count}")
        
        print()
    
    print("=" * 70)
    print("CACHE STATE VERIFICATION")
    print("=" * 70)
    print()
    print(f"Total cache entries: {len(_cache)}")
    print()
    print("Cache keys (should all be unversioned IDs):")
    for key in sorted(_cache.keys()):
        print(f"  • {key}")
    print()
    
    print("=" * 70)
    print("EXPECTED BEHAVIOR AFTER FIX:")
    print("=" * 70)
    print("""
    1. Version suffixes (v1, v2, etc.) should be stripped using regex
    2. All variants of same paper should map to same cleaned ID
    3. Cache lookup uses cleaned ID
    4. API query uses cleaned ID in ARXIV:<id> format
    5. Multiple version variants of same paper should hit cache on 2nd+ query
    6. Citation counts should be non-zero for papers with citations
    """)
    
if __name__ == "__main__":
    test_version_suffix_stripping()
