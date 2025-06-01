from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class PriceHistoryRequest(BaseModel):
    url: HttpUrl

class PricePoint(BaseModel):
    date: str
    price: float

class PriceHistoryResponse(BaseModel):
    asin: str
    history: List[PricePoint]

class ErrorResponse(BaseModel):
    detail: str 