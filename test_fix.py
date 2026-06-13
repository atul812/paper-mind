#!/usr/bin/env python
"""
Diagnostic script to test the pipeline fixes
"""
import sys
import traceback

def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    try:
        from backend.data_fetch import fetch_papers
        from backend.citation_fetch import enrich_with_citations
        from backend.time_windows import compute_time_windows
        from ml.topic_modeling import run_topic_modeling
        from backend.tfidf_scoring import compute_tfidf_scores
        from backend.velocity import compute_velocity
        from backend.citation_velocity import compute_citation_velocity
        from backend.momentum import compute_momentum
        from backend.forecasting import forecast_topics
        print("✓ All imports successful\n")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        traceback.print_exc()
        return False

def test_data_initialization():
    """Test that papers are initialized with correct fields"""
    print("Testing data initialization...")
    try:
        from backend.data_fetch import fetch_papers
        print("  Fetching sample papers...")
        papers = fetch_papers("machine learning", max_results=10)
        
        if not papers:
            print("  ✗ No papers fetched")
            return False
            
        sample_paper = papers[0]
        required_fields = ["id", "title", "abstract", "published_date", "topic_id", "citation_count", "influential_citation_count"]
        
        print(f"  Sample paper fields: {list(sample_paper.keys())}")
        for field in required_fields:
            if field not in sample_paper:
                print(f"  ✗ Missing field: {field}")
                return False
            print(f"    ✓ {field}: {type(sample_paper[field]).__name__}")
        
        print(f"  ✓ Data initialization correct (fetched {len(papers)} papers)\n")
        return True
    except Exception as e:
        print(f"✗ Data initialization error: {e}")
        traceback.print_exc()
        return False

def test_topic_modeling():
    """Test topic modeling on sample data"""
    print("Testing topic modeling...")
    try:
        from ml.topic_modeling import run_topic_modeling
        
        # Use small sample with diverse content
        papers = [
            {
                "abstract": "Federated learning enables privacy-preserving machine learning across distributed devices.",
                "topic_id": -1,
                "title": "FL paper 1"
            },
            {
                "abstract": "Secure aggregation protocols improve privacy in federated learning systems.",
                "topic_id": -1,
                "title": "FL paper 2"
            },
            {
                "abstract": "Deep neural networks achieve state-of-the-art performance on image classification tasks.",
                "topic_id": -1,
                "title": "DNN paper 1"
            },
            {
                "abstract": "Convolutional neural networks process images through multiple layers of learned filters.",
                "topic_id": -1,
                "title": "DNN paper 2"
            },
            {
                "abstract": "Reinforcement learning agents learn to make decisions through interaction with environment.",
                "topic_id": -1,
                "title": "RL paper 1"
            },
        ]
        
        print(f"  Processing {len(papers)} papers...")
        tagged_papers, topic_labels = run_topic_modeling(papers)
        
        print(f"  Topics identified: {len(topic_labels)}")
        print(f"  Topic map: {topic_labels}")
        
        # Check that all papers have topic_ids
        for i, paper in enumerate(tagged_papers):
            if "topic_id" not in paper:
                print(f"  ✗ Paper {i} missing topic_id")
                return False
            print(f"    Paper {i}: topic_id={paper['topic_id']}")
        
        print(f"  ✓ Topic modeling successful\n")
        return True
    except Exception as e:
        print(f"✗ Topic modeling error: {e}")
        traceback.print_exc()
        return False

def test_tfidf_and_velocity():
    """Test TFIDF and velocity computation"""
    print("Testing TFIDF and velocity computation...")
    try:
        from backend.tfidf_scoring import compute_tfidf_scores
        from backend.velocity import compute_velocity
        
        # Create sample papers with topics and windows
        papers = [
            {"abstract": "Federated learning privacy", "topic_id": 0, "window": "2024_W0"},
            {"abstract": "Federated learning secure", "topic_id": 0, "window": "2024_W1"},
            {"abstract": "Federated learning efficient", "topic_id": 0, "window": "2025_W0"},
            {"abstract": "Deep learning neural networks", "topic_id": 1, "window": "2024_W0"},
            {"abstract": "Deep learning training", "topic_id": 1, "window": "2024_W1"},
            {"abstract": "Deep learning optimization", "topic_id": 1, "window": "2025_W0"},
        ]
        
        print(f"  Computing TFIDF for {len(papers)} papers...")
        tfidf_matrix = compute_tfidf_scores(papers)
        
        print(f"  TFIDF matrix shape: {tfidf_matrix.shape}")
        print(f"  TFIDF columns: {list(tfidf_matrix.columns)}")
        print(f"  TFIDF matrix:\n{tfidf_matrix}")
        
        if tfidf_matrix.empty:
            print("  ✗ TFIDF matrix is empty")
            return False
        
        if "topic_id" not in tfidf_matrix.columns:
            print("  ✗ TFIDF matrix missing topic_id column")
            return False
        
        print(f"  Computing velocity...")
        velocity = compute_velocity(tfidf_matrix)
        
        print(f"  Velocity results: {len(velocity)} topics")
        for v in velocity:
            print(f"    Topic {v['topic_id']}: velocity={v['velocity']:.4f}, trend={v['trend']}")
        
        print(f"  ✓ TFIDF and velocity computation successful\n")
        return True
    except Exception as e:
        print(f"✗ TFIDF/velocity error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Paper-Mind Pipeline Diagnostic Tests")
    print("=" * 60 + "\n")
    
    tests = [
        test_imports,
        test_data_initialization,
        test_topic_modeling,
        test_tfidf_and_velocity,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result))
        except Exception as e:
            print(f"FATAL ERROR in {test.__name__}: {e}")
            traceback.print_exc()
            results.append((test.__name__, False))
    
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(r for _, r in results)
    print("\n" + ("✓ All tests passed!" if all_passed else "✗ Some tests failed"))
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
