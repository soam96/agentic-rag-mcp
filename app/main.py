from app.mcp import MCPMessage
from app.storage.store import ChunkStore
from app.embedder import MockEmbedder
from app.ingestion_agent import IngestionAgent
from app.retrieval_agent import RetrievalAgent
from app.llm_response_agent import LLMResponseAgent

# -------------------------------
# Mock LLM Client
# -------------------------------
class MockLLM:
    """
    Simple mock LLM for testing.
    Returns a snippet if 'KPIs include' is found, else a generic mock answer.
    """
    def generate(self, query: str, context: str) -> str:
        if "KPIs include" in context:
            idx = context.find("KPIs include")
            snippet = context[idx: idx + 200]
            return "(extracted) " + snippet
        return "(mock answer) Based on provided documents."

# -------------------------------
# Demo flow
# -------------------------------
def demo_flow(file_path: str, user_query: str):
    # Initialize storage and agents
    store = ChunkStore(path='data/chunks.json')
    ingester = IngestionAgent(store)

    # -------------------------------
    # Step 1: Ingest file
    # -------------------------------
    m_indexed = ingester.ingest_file(file_path)
    print('MCP from ingestion:', m_indexed.to_dict())

    # -------------------------------
    # Step 2: Build retrieval index
    # -------------------------------
    texts = [v['text'] for v in store.chunks.values()]
    ids = list(store.chunks.keys())

    embedder = MockEmbedder()
    retr = RetrievalAgent(embedder, store)
    retr.build_index(texts, ids)

    # -------------------------------
    # Step 3: Query retrieval agent
    # -------------------------------
    results = retr.query(user_query, top_k=5)
    context_msg = MCPMessage(
        sender='RetrievalAgent',
        receiver='LLMResponseAgent',
        type='CONTEXT_RESPONSE',
        payload={'top_chunks': results, 'query': user_query, 'origin': 'User'}
    )

    # -------------------------------
    # Step 4: LLM response agent
    # -------------------------------
    llm_agent = LLMResponseAgent(MockLLM())
    final = llm_agent.handle_context_response(context_msg)

    # -------------------------------
    # Step 5: Output final answer
    # -------------------------------
    print('\nFINAL MCP MESSAGE:')
    print(final)

# -------------------------------
# Run demo if executed directly
# -------------------------------
if __name__ == '__main__':
    demo_flow('examples/sample.txt', 'What are the KPIs?')
