from __future__ import annotations

import os
from pathlib import Path
from typing import Any, List

import chromadb
from chromadb.utils import embedding_functions

class BookContextMemory:
    """RAG-based context memory for BookFactory chapters."""

    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root).resolve()
        self.db_path = self.project_root / "build" / ".chroma_db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB persistent client
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Use a local embedding model
        # Note: all-MiniLM-L6-v2 is the default for SentenceTransformerEmbeddingFunction
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="book_chapters",
            embedding_function=self.emb_fn
        )

    def _chunk_markdown(self, text: str) -> List[str]:
        """Split markdown text into chunks based on '##' headers."""
        # Simple split by '##', keeping the headers
        chunks = []
        lines = text.splitlines()
        current_chunk = []
        
        for line in lines:
            if line.startswith("## ") and current_chunk:
                chunks.append("\n".join(current_chunk).strip())
                current_chunk = [line]
            else:
                current_chunk.append(line)
        
        if current_chunk:
            chunks.append("\n".join(current_chunk).strip())
            
        return [c for c in chunks if c]

    def index_chapter(self, chapter_id: str, file_path: str | Path) -> None:
        """Indexes a chapter file into ChromaDB."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Chapter file not found: {path}")
            
        content = path.read_text(encoding="utf-8")
        chunks = self._chunk_markdown(content)
        
        ids = [f"{chapter_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"chapter_id": chapter_id} for _ in range(len(chunks))]
        
        self.collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas
        )

    def retrieve_context(self, query: str, n_results: int = 3) -> str:
        """Retrieves relevant context chunks for a given query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        if not documents:
            return "No relevant context found."
            
        context_parts = []
        for doc, meta in zip(documents, metadatas):
            cid = meta.get("chapter_id", "unknown")
            context_parts.append(f"--- Kaynak: {cid} ---\n{doc}")
            
        return "\n\n".join(context_parts)
