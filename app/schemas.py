from pydantic import BaseModel

class SupportResponse(BaseModel):
    category: str
    summary: str