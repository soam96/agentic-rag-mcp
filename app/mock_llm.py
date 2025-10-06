# app/mock_llm.py

class MockLLM:
    """
    Simple mock LLM that returns a canned response for testing.
    In production you would replace this with an OpenAI / HuggingFace client.
    """

    def generate(self, query: str, context: str) -> str:
        return (
            f"[MockLLM Answer]\n"
            f"Query: {query}\n"
            f"Context Used:\n{context[:200]}..."
        )
