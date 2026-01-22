from typing import Optional, List
from pydantic import BaseModel, Field


class KeywordAnalysis(BaseModel):
    matched_keywords: List[str] = Field(default_factory=list, description="Palavras-chave que foram encontradas e usadas")
    produtivo_score: int = Field(default=0, description="Quantidade de keywords de produtivo encontradas")
    improdutivo_score: int = Field(default=0, description="Quantidade de keywords de improdutivo encontradas")
    total_keywords: int = Field(default=0, description="Total de keywords extraídas")


class ProcessingDetails(BaseModel):
    classification_method: str = Field(..., description="Método usado: 'keywords_only', 'ai', 'fallback'")
    used_full_text: Optional[bool] = Field(None, description="Se enviou texto completo para IA")
    used_ai: Optional[bool] = Field(None, description="Se usou IA na classificação")
    used_fallback: Optional[bool] = Field(None, description="Se usou fallback baseado em keywords")
    keyword_analysis: KeywordAnalysis


class NLPDebug(BaseModel):
    detected_keywords: str
    keyword_analysis: Optional[KeywordAnalysis] = None


class ProcessResponseData(BaseModel):
    filename: Optional[str] = None
    category: str
    confidence_score: float
    summary: str
    suggested_response: Optional[str] = None
    reason: Optional[str] = Field(None, description="Razão detalhada da classificação")
    nlp_debug: NLPDebug
    processing_details: ProcessingDetails


class ProcessResponse(BaseModel):
    status: str
    data: ProcessResponseData


class ErrorResponse(BaseModel):
    status: str
    error_code: str
    message: str
    details: Optional[dict] = None
