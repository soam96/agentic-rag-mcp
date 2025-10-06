import os, json
from typing import List, Dict
from uuid import uuid4

class ChunkStore:
    def __init__(self, path='data/chunks.json'):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            try:
                with open(path,'r',encoding='utf8') as f:
                    self.chunks = json.load(f)
            except Exception:
                self.chunks = {}
        else:
            self.chunks = {}

    def add_chunk(self, text: str, meta: Dict) -> str:
        cid = str(uuid4())
        self.chunks[cid] = {"text": text, "meta": meta}
        return cid

    def save(self):
        with open(self.path,'w',encoding='utf8') as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=2)

    def get(self, cid: str):
        return self.chunks.get(cid)

    def all_texts(self):
        return [v['text'] for v in self.chunks.values()]

    def all_items(self):
        return list(self.chunks.items())
