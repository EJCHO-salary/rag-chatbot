import tempfile
from ragchat.search import BM25Search

def test_search_engine_basic():
    search_engine = BM25Search()
    # Add a third chunk to avoid BM25 issues with small corpora
    chunks = [
        "The quick brown fox jumps over the lazy dog",
        "I love coding in Python",
        "The weather is nice today"
    ]
    search_engine.fit(chunks)
    
    # Query related to first chunk
    results = search_engine.search("quick fox", n=1)
    assert len(results) == 1
    assert "quick" in results[0].lower()

    # Query related to second chunk
    results = search_engine.search("python", n=1)
    assert len(results) == 1
    assert "python" in results[0].lower()

def test_save_load():
    with tempfile.TemporaryDirectory() as tmpdir:
        search_engine = BM25Search(data_dir=tmpdir)
        chunks = [
            "Document 1 with some content",
            "Document 2 is about apples",
            "Document 3 is about oranges"
        ]
        search_engine.fit(chunks)
        search_engine.save("test_index.json")
        
        # New search engine to load the index
        new_search_engine = BM25Search(data_dir=tmpdir)
        new_search_engine.load("test_index.json")
        
        assert new_search_engine.chunks == chunks
        results = new_search_engine.search("apples", n=1)
        assert len(results) == 1
        assert "apples" in results[0]

def test_empty_search():
    search_engine = BM25Search()
    results = search_engine.search("nothing")
    assert results == []

def test_fit_empty_chunks():
    search_engine = BM25Search()
    search_engine.fit([])
    assert search_engine.bm25 is None
    results = search_engine.search("something")
    assert results == []
