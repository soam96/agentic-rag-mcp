from typing import List

class BaseEmbedder:
    def embed(self, texts: List[str]):
        raise NotImplementedError()

# Simple mock embedder that uses hashed vectors (deterministic)
import numpy as np
class MockEmbedder(BaseEmbedder):
    def embed(self, texts):
        embs = []
        for t in texts:
            h = abs(hash(t)) % (10**8)
            # create a small vector from digits
            vec = [(h >> (8*i)) & 0xFF for i in range(8)]
            embs.append(np.array(vec, dtype='float32'))
        return embs
