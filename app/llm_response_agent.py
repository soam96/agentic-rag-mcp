# app/llm_response_agent.py

class LLMResponseAgent:
    def __init__(self, llm):
        self.llm = llm

    def handle_context_response(self, msg) -> dict:
        """
        Handles CONTEXT_RESPONSE messages from the RetrievalAgent
        and produces a final ANSWER message.
        msg can be either:
        - an MCPMessage object (with .payload attribute)
        - or a plain dict (with ["payload"] key)
        """

        # Handle both dict and MCPMessage
        if hasattr(msg, "payload"):
            payload = msg.payload
            trace_id = getattr(msg, "trace_id", None)
        else:
            payload = msg.get("payload", {})
            trace_id = msg.get("trace_id")

        # Extract query + chunks
        top_chunks = payload.get("top_chunks", [])
        query = payload.get("query", "")

        # Normalize chunks into readable context
        context_texts = []
        for c in top_chunks:
            if isinstance(c, dict):
                source = c.get("meta", {}).get("source", "unknown")
                text = c.get("text", "")
                context_texts.append(f"SOURCE: {source}\n{text}")
            else:
                # Fallback if chunk is just a string
                context_texts.append(str(c))

        context_text = "\n\n---\n\n".join(context_texts)

        # Ask the LLM
        answer = self.llm.generate(query, context_text)

        # Return MCP-style dict response
        return {
            "sender": "LLMResponseAgent",
            "receiver": "User",
            "type": "ANSWER",
            "trace_id": trace_id,
            "payload": {
                "answer": answer,
                "context_used": context_texts
            },
        }
