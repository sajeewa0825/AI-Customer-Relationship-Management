from pydantic import BaseModel
from typing import Optional


class document(BaseModel):
    company_id: int
    content: str
    document_meta: Optional[str] = None

class documentCreate(document):
    pass

class documentResponse(document):
    pass

    class Config:
        from_attributes = True

