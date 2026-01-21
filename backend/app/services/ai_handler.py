import json
import os
from typing import Dict, Any
from google import genai

from app.utils.exceptions import AIAPIException
from app.utils.logger import logger


_gemini_client = None


def _get_gemini_client():
    global _gemini_client
    if _gemini_client is not None:
        return _gemini_client
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise AIAPIException("GEMINI_API_KEY não configurada")
    
    _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client


def analyze_email(raw_text: str, nlp_keywords: str) -> Dict[str, Any]:
    client = _get_gemini_client()
    
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    
    try:
        prompt = f"""Atue como um sistema de triagem de emails corporativos para uma empresa financeira.
Analise o seguinte email e retorne um JSON.

TEXTO ORIGINAL:
{raw_text}

CONTEXTO NLP (PALAVRAS-CHAVE PROCESSADAS):
{nlp_keywords}

Classificações:
- Produtivo: Emails que requerem ação ou resposta específica (solicitações de suporte, atualizações sobre casos, dúvidas sobre sistema, pedidos de documentos, etc.)
- Improdutivo: Emails que não necessitam ação imediata (mensagens de felicitações, agradecimentos genéricos, spam, etc.)

Responda EXCLUSIVAMENTE neste formato JSON:
{{
    "categoria": "Produtivo" ou "Improdutivo",
    "razao": "Breve explicação em uma frase sobre por que foi classificado assim",
    "sugestao_resposta": "Se Produtivo, escreva uma resposta formal e profissional em português brasileiro. Se Improdutivo, retorne null"
}}

IMPORTANTE: Responda APENAS em JSON válido, sem markdown, sem explicações adicionais."""
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        content = response.text.strip()
        
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        result = json.loads(content)
        
        categoria = result.get('categoria', '').strip()
        razao = result.get('razao', '').strip()
        sugestao_resposta = result.get('sugestao_resposta')
        
        if categoria not in ['Produtivo', 'Improdutivo']:
            raise AIAPIException("Categoria inválida retornada pela API")
        
        confidence_score = _calculate_confidence_score(categoria, razao)
        
        summary = razao if razao else f"Email classificado como {categoria}"
        
        return {
            'category': categoria,
            'reason': razao,
            'suggested_response': sugestao_resposta if sugestao_resposta else None,
            'confidence_score': confidence_score,
            'summary': summary
        }
    
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao parsear JSON da resposta do Gemini: {str(e)}")
        raise AIAPIException("Resposta inválida da API de IA")
    
    except Exception as e:
        error_message = str(e).lower()
        logger.error(f"Erro na API Gemini: {str(e)}")
        
        if 'timeout' in error_message or 'deadline' in error_message:
            raise AIAPIException("Timeout na comunicação com a API de IA. Tente novamente.")
        
        if 'rate limit' in error_message or 'quota' in error_message:
            raise AIAPIException("Limite de requisições excedido. Tente novamente em alguns instantes.")
        
        if 'api key' in error_message or 'authentication' in error_message:
            raise AIAPIException("Chave da API inválida ou não configurada")
        
        raise AIAPIException(f"Erro na API de IA: {str(e)}")


def _calculate_confidence_score(categoria: str, razao: str) -> float:
    base_score = 0.85
    
    if len(razao) > 20:
        base_score += 0.05
    
    if categoria == 'Produtivo' and 'solicit' in razao.lower():
        base_score += 0.05
    elif categoria == 'Improdutivo' and any(word in razao.lower() for word in ['felicitaç', 'agradec', 'cumpriment']):
        base_score += 0.05
    
    return min(base_score, 0.99)
