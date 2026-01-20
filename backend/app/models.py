from typing import Optional
from pydantic import BaseModel, Field


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=50000, description="Texto do email para análise")


class NLPDebug(BaseModel):
    detected_keywords: str


class ProcessResponseData(BaseModel):
    filename: Optional[str] = None
    category: str
    confidence_score: float
    summary: str
    suggested_response: Optional[str] = None
    nlp_debug: NLPDebug


class ProcessResponse(BaseModel):
    status: str
    data: ProcessResponseData


class ErrorResponse(BaseModel):
    status: str
    error_code: str
    message: str
    details: Optional[dict] = None
