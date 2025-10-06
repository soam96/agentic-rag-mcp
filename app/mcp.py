from typing import Dict, Any
from uuid import uuid4

class MCPMessage:
    def __init__(self, sender: str, receiver: str, type: str, payload: Dict[str, Any], trace_id: str = None):
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.payload = payload
        self.trace_id = trace_id or str(uuid4())

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type,
            "trace_id": self.trace_id,
            "payload": self.payload,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(d["sender"], d["receiver"], d["type"], d["payload"], d.get("trace_id"))
