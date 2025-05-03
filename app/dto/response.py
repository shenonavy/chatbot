from pydantic import BaseModel

class ResponseModel(BaseModel):
    status: str = "success"
    response: str = ""
