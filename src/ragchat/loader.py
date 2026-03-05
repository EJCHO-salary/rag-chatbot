from pathlib import Path
from typing import List, Dict, Any, Optional
import pypdf
from dataclasses import dataclass, asdict

@dataclass
class DocumentChunk:
    text: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class DocumentLoader:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_file(self, file_path: Path) -> List[DocumentChunk]:
        """Loads a file and returns a list of document chunks."""
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            text = self._load_pdf(file_path)
        elif suffix in [".txt", ".md"]:
            text = self._load_text(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

        return self.split_text(text, metadata={"source": str(file_path)})

    def _load_text(self, file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_pdf(self, file_path: Path) -> str:
        text = ""
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def split_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[DocumentChunk]:
        """Splits text into chunks of roughly chunk_size characters."""
        if not text:
            return []
        
        metadata = metadata or {}
        chunks = []
        
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            # Create a copy of metadata to avoid shared references if needed
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "start_char": start,
                "end_char": min(end, text_len)
            })
            
            chunks.append(DocumentChunk(text=chunk_text, metadata=chunk_metadata))
            
            # Move start forward by chunk_size - overlap
            if end >= text_len:
                break
            start += (self.chunk_size - self.chunk_overlap)
            
        return chunks
