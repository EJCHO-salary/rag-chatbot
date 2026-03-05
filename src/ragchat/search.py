import json
import logging
from pathlib import Path
from typing import List, Optional

from rank_bm25 import BM25Okapi

logger = logging.getLogger(__name__)

class BM25Search:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.data_dir / "index.json"
        self.chunks: List[str] = []
        self.bm25: Optional[BM25Okapi] = None

    def _tokenize(self, text: str) -> List[str]:
        # Simple whitespace tokenization with lowercase and stripping punctuation
        return "".join(c if c.isalnum() or c.isspace() else " " for c in text.lower()).split()

    def fit(self, chunks: List[str]):
        """Build the BM25 index from a list of chunks."""
        if not chunks:
            logger.warning("Attempted to fit BM25 with empty chunks list.")
            return
        
        self.chunks = chunks
        tokenized_corpus = [self._tokenize(chunk) for chunk in chunks]
        # Debug print to see tokenized corpus
        # print(f"DEBUG: tokenized_corpus={tokenized_corpus}")
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str, n: int = 5) -> List[str]:
        """Return the top n chunks for a query."""
        if not self.bm25 or not self.chunks:
            logger.warning("Search called but index is empty or not built.")
            return []
        
        tokenized_query = self._tokenize(query)
        # print(f"DEBUG: tokenized_query={tokenized_query}")
        if not tokenized_query:
            return []
            
        # rank-bm25's get_top_n:
        # get_top_n(tokenized_query, corpus, n=5)
        # where corpus is the ORIGINAL list of documents (not tokenized)
        top_n = self.bm25.get_top_n(tokenized_query, self.chunks, n=n)
        return top_n

    def save(self, filename: Optional[str] = None):
        """Save chunks to a JSON file."""
        target_file = self.data_dir / filename if filename else self.index_file
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(self.chunks)} chunks to {target_file}")

    def load(self, filename: Optional[str] = None):
        """Load chunks from a JSON file and rebuild index."""
        target_file = self.data_dir / filename if filename else self.index_file
        if not target_file.exists():
            logger.error(f"Index file {target_file} does not exist.")
            return

        with open(target_file, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        
        if self.chunks:
            self.fit(self.chunks)
            logger.info(f"Loaded {len(self.chunks)} chunks and rebuilt index.")
        else:
            logger.warning("Loaded empty chunks list.")
