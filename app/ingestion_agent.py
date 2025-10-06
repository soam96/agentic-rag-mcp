from app.mcp import MCPMessage
from app.parsers import *
from app.storage.store import ChunkStore

class IngestionAgent:
    def __init__(self, chunk_store: ChunkStore):
        self.store = chunk_store

    def ingest_file(self, file_path: str) -> MCPMessage:
        suffix = file_path.split('.')[-1].lower()
        if suffix == 'pdf':
            parts = parse_pdf(file_path)
        elif suffix in ('pptx', 'ppt'):
            parts = parse_pptx(file_path)
        elif suffix in ('docx', 'doc'):
            parts = parse_docx(file_path)
        elif suffix in ('csv',):
            parts = parse_csv(file_path)
        else:
            parts = parse_txt_md(file_path)

        chunk_ids = []
        for p in parts:
            text = p.get('text','')
            if not text or len(text.strip())==0:
                continue
            cid = self.store.add_chunk(text, meta={"source": file_path, **{k:v for k,v in p.items() if k!='text'}})
            chunk_ids.append(cid)

        self.store.save()
        payload = {"chunk_ids": chunk_ids, "source": file_path}
        return MCPMessage("IngestionAgent","RetrievalAgent","CONTEXT_INDEXED", payload)
