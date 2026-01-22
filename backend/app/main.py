from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()

from app.models import ProcessResponse, ErrorResponse
from app.services.file_reader import read_file
from app.services.nlp_engine import extract_keywords
from app.services.ai_handler import analyze_email
from app.utils.exceptions import (
    EmailClassifierException,
    InvalidFileException,
    InvalidTextException,
    NLPProcessingException,
    AIAPIException
)
from app.utils.validators import validate_text
from app.config import CORS_ORIGINS, RATE_LIMIT_PER_MINUTE
from app.utils.logger import logger

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Email Classifier API",
    description="API para classificação automática de emails usando IA e NLP",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if '*' not in CORS_ORIGINS else ['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['Content-Type', 'Authorization'],
)


@app.exception_handler(InvalidFileException)
async def invalid_file_handler(request: Request, exc: InvalidFileException):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "error_code": "INVALID_FILE",
            "message": str(exc),
            "details": {}
        }
    )


@app.exception_handler(InvalidTextException)
async def invalid_text_handler(request: Request, exc: InvalidTextException):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "error_code": "INVALID_TEXT",
            "message": str(exc),
            "details": {}
        }
    )


@app.exception_handler(NLPProcessingException)
async def nlp_processing_handler(request: Request, exc: NLPProcessingException):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_code": "NLP_PROCESSING_ERROR",
            "message": str(exc),
            "details": {}
        }
    )


@app.exception_handler(AIAPIException)
async def ai_api_handler(request: Request, exc: AIAPIException):
    status_code = 503 if "timeout" in str(exc).lower() or "rate limit" in str(exc).lower() else 500
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "error_code": "AI_API_ERROR",
            "message": str(exc),
            "details": {}
        }
    )


@app.exception_handler(EmailClassifierException)
async def email_classifier_handler(request: Request, exc: EmailClassifierException):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_code": "CLASSIFIER_ERROR",
            "message": str(exc),
            "details": {}
        }
    )


@app.get("/")
async def root():
    return {"msg": "Email Classifier API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/v1/process", response_model=ProcessResponse)
@limiter.limit(f"{RATE_LIMIT_PER_MINUTE}/minute")
async def process_email(
    request: Request,
    file: Union[UploadFile, None] = File(None),
    text: Union[str, None] = Form(None)
):
    try:
        raw_text = None
        filename = None
        
        if file:
            filename = file.filename
            raw_text = await read_file(file)
        elif text:
            validate_text(text)
            raw_text = text
        else:
            raise HTTPException(
                status_code=400,
                detail="Forneça um arquivo (campo 'file') ou texto (campo 'text') via multipart/form-data"
            )
        
        if not raw_text or not raw_text.strip():
            raise HTTPException(status_code=400, detail="Conteúdo não pode estar vazio")
        
        logger.info(f"Processando email: {filename or 'texto direto'}")
        
        nlp_keywords = extract_keywords(raw_text)
        logger.info(f"Keywords extraídas: {nlp_keywords[:100]}...")
        
        ai_result = analyze_email(raw_text, nlp_keywords)
        logger.info(f"Email classificado como: {ai_result['category']}")
        
        # Determinar método de classificação
        classification_method = 'ai'
        if ai_result.get('used_keywords_only'):
            classification_method = 'keywords_only'
        elif ai_result.get('used_fallback'):
            classification_method = 'fallback'
        
        # Preparar detalhes de processamento
        keyword_analysis = ai_result.get('keyword_analysis', {
            'matched_keywords': [],
            'produtivo_score': 0,
            'improdutivo_score': 0,
            'total_keywords': len(nlp_keywords.split())
        })
        
        processing_details = {
            "classification_method": classification_method,
            "used_full_text": ai_result.get('used_full_text'),
            "used_ai": ai_result.get('used_ai', False),
            "used_fallback": ai_result.get('used_fallback', False),
            "keyword_analysis": keyword_analysis
        }
        
        response_data = {
            "status": "success",
            "data": {
                "filename": filename,
                "category": ai_result['category'],
                "confidence_score": ai_result['confidence_score'],
                "summary": ai_result['summary'],
                "reason": ai_result.get('reason', ai_result['summary']),
                "suggested_response": ai_result['suggested_response'],
                "nlp_debug": {
                    "detected_keywords": nlp_keywords,
                    "keyword_analysis": keyword_analysis
                },
                "processing_details": processing_details
            }
        }
        
        return ProcessResponse(**response_data)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado no processamento: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )
