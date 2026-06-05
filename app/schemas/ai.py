from typing import Optional

from pydantic import BaseModel


class SuggestRequest(BaseModel):
    type: str
    context: Optional[str] = ""
    note: Optional[int] = 5
    api_key: Optional[str] = None
