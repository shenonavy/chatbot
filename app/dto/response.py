from pydantic import BaseModel
from typing import Literal
from typing import Optional

class ResponseModel(BaseModel):
    status: str = "success"
    response: str = ""
    source_type: Optional[Literal["knowledge_base", "web_search", "unknown", "human", "agent"]] = None
