from typing import List, Dict
import numpy as np

class RetrievalAgent:
    def __init__(self, embedder, chunk_store):
        self.embedder = embedder
        self.chunk_store = chunk_store
        self.index_vectors = None
        self.id_map = []

    def build_index(self, chunk_texts: List[str], ids: List[str]):
        vecs = self.embedder.embed(chunk_texts)
        self.index_vectors = np.vstack([v for v in vecs]).astype('float32')
        self.id_map = ids

    def query(self, q: str, top_k: int = 5) -> List[Dict]:
        qv = self.embedder.embed([q])[0].astype('float32')
        # compute L2 distances
        dists = ((self.index_vectors - qv)**2).sum(axis=1)
        idxs = dists.argsort()[:top_k]
        results = []
        for idx in idxs:
            cid = self.id_map[int(idx)]
            chunk = self.chunk_store.get(cid)
            results.append({"chunk_id": cid, "text": chunk['text'], "meta": chunk['meta']})
        return results
