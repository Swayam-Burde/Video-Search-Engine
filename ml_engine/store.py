# File: ml_engine/store.py
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

class VectorDB:
    def __init__(self):
        # Local persistent storage
        self.client = QdrantClient(path="./qdrant_db")
        
        # Ensure collections exist on startup
        self._ensure_collection("visual_search", 512)
        self._ensure_collection("audio_search", 512)

    def _ensure_collection(self, name, size):
        """Creates collection if it doesn't exist"""
        if not self.client.collection_exists(name):
            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=size, distance=Distance.COSINE)
            )

    def reset_db(self):
        """⚠️ Deletes all data and re-creates empty collections"""
        print(f"🧹 Wiping database...")
        # Delete old collections
        self.client.delete_collection("visual_search")
        self.client.delete_collection("audio_search")
        
        # Re-create fresh ones
        self._ensure_collection("visual_search", 512)
        self._ensure_collection("audio_search", 512)
        print("✨ Database is clean and ready for new video.")

    def upload_vectors(self, vectors, payloads, collection_name):
        """
        vectors: list of lists (embeddings)
        payloads: list of dicts (metadata like timestamp, text)
        """
        # Batch upload for speed
        self.client.upload_collection(
            collection_name=collection_name,
            vectors=vectors,
            payload=payloads
        )

    def search(self, query_vector, collection_name, top_k=3):
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k
        )