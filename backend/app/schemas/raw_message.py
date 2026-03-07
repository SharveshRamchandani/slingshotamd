from pydantic import BaseModel
from typing import Dict, Any, Optional

class RawMessage(BaseModel):
    user_id: int
    source: str
    data: Dict[str, Any]
    processed: bool = False
