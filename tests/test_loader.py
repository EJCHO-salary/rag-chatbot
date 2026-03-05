import pytest
from ragchat.loader import DocumentLoader

def test_load_text_file(tmp_path):
    file_path = tmp_path / "test.txt"
    content = "Hello world! This is a test."
    file_path.write_text(content)

    loader = DocumentLoader(chunk_size=10, chunk_overlap=0)
    chunks = loader.load_file(file_path)

    assert len(chunks) > 0
    assert "".join([c.text for c in chunks]) == content
    assert chunks[0].metadata["source"] == str(file_path)

def test_split_text_no_overlap():
    loader = DocumentLoader(chunk_size=5, chunk_overlap=0)
    text = "1234567890"
    chunks = loader.split_text(text)
    
    assert len(chunks) == 2
    assert chunks[0].text == "12345"
    assert chunks[1].text == "67890"

def test_split_text_with_overlap():
    loader = DocumentLoader(chunk_size=10, chunk_overlap=5)
    text = "012345678901234"
    chunks = loader.split_text(text)
    
    # Chunk 1: [0:10] -> "0123456789"
    # Chunk 2: [5:15] -> "5678901234"
    assert len(chunks) == 2
    assert chunks[0].text == "0123456789"
    assert chunks[1].text == "5678901234"

def test_load_md_file(tmp_path):
    file_path = tmp_path / "test.md"
    content = "# Title\n\n- item 1\n- item 2"
    file_path.write_text(content)

    loader = DocumentLoader()
    chunks = loader.load_file(file_path)
    
    assert len(chunks) == 1
    assert chunks[0].text == content

def test_unsupported_format(tmp_path):
    file_path = tmp_path / "test.jpg"
    file_path.write_text("not an image")
    
    loader = DocumentLoader()
    with pytest.raises(ValueError, match="Unsupported file format"):
        loader.load_file(file_path)
