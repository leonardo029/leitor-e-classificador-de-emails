import json
import os
from typing import Dict, Any, Optional
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


# Palavras-chave de alta confiança para classificação
PRODUTIVO_KEYWORDS = {
    'solicit', 'pedid', 'requer', 'necessit', 'urgent',
    'problema', 'erro', 'suport', 'ajud', 'duvida',
    'boleto', 'fatur', 'pagament', 'venciment', 'segund',
    'atualiz', 'status', 'caso', 'protocol', 'ticket'
}

IMPRODUTIVO_KEYWORDS = {
    'feliz', 'natal', 'ano novo', 'parabens', 'agradec',
    'cumpriment', 'saudacoes', 'obrigad', 'obrigado',
    'felicitacoes', 'comemor', 'celebr'
}


def pre_classify_with_keywords(keywords: str) -> Optional[Dict[str, Any]]:
    """
    Tenta classificar usando apenas keywords.
    Retorna None se não conseguir (caso ambíguo).
    """
    keyword_list = set(keywords.lower().split())
    
    matched_produtivo = keyword_list & PRODUTIVO_KEYWORDS
    matched_improdutivo = keyword_list & IMPRODUTIVO_KEYWORDS
    
    produtivo_score = len(matched_produtivo)
    improdutivo_score = len(matched_improdutivo)
    
    # Se diferença for grande, classificar sem IA
    if produtivo_score >= 2 and improdutivo_score == 0:
        return {
            'category': 'Produtivo',
            'reason': f'Identificado como produtivo através de {produtivo_score} palavras-chave relevantes: {", ".join(sorted(matched_produtivo))}',
            'confidence_score': min(0.75 + (produtivo_score * 0.05), 0.90),
            'summary': f'Email identificado como produtivo por {produtivo_score} palavras-chave relevantes',
            'used_keywords_only': True,
            'keyword_analysis': {
                'matched_keywords': sorted(list(matched_produtivo)),
                'produtivo_score': produtivo_score,
                'improdutivo_score': improdutivo_score,
                'total_keywords': len(keyword_list)
            }
        }
    elif improdutivo_score >= 2 and produtivo_score == 0:
        return {
            'category': 'Improdutivo',
            'reason': f'Identificado como improdutivo através de {improdutivo_score} palavras-chave relevantes: {", ".join(sorted(matched_improdutivo))}',
            'confidence_score': min(0.75 + (improdutivo_score * 0.05), 0.90),
            'summary': f'Email identificado como improdutivo por {improdutivo_score} palavras-chave relevantes',
            'used_keywords_only': True,
            'keyword_analysis': {
                'matched_keywords': sorted(list(matched_improdutivo)),
                'produtivo_score': produtivo_score,
                'improdutivo_score': improdutivo_score,
                'total_keywords': len(keyword_list)
            }
        }
    
    return None  # Caso ambíguo, precisa de IA


def analyze_with_keywords_fallback(keywords: str, raw_text: str) -> Dict[str, Any]:
    """
    Fallback: classifica usando apenas keywords quando IA falha.
    """
    keyword_list = set(keywords.lower().split())
    
    matched_produtivo = keyword_list & PRODUTIVO_KEYWORDS
    matched_improdutivo = keyword_list & IMPRODUTIVO_KEYWORDS
    
    produtivo_score = len(matched_produtivo)
    improdutivo_score = len(matched_improdutivo)
    
    if produtivo_score > improdutivo_score:
        category = 'Produtivo'
        confidence = min(0.60 + (produtivo_score * 0.05), 0.80)
        matched_keywords = sorted(list(matched_produtivo))
        reason = f'Classificado como produtivo baseado em {produtivo_score} palavras-chave (fallback): {", ".join(matched_keywords)}'
    elif improdutivo_score > produtivo_score:
        category = 'Improdutivo'
        confidence = min(0.60 + (improdutivo_score * 0.05), 0.80)
        matched_keywords = sorted(list(matched_improdutivo))
        reason = f'Classificado como improdutivo baseado em {improdutivo_score} palavras-chave (fallback): {", ".join(matched_keywords)}'
    else:
        # Empate ou nenhuma keyword relevante - usar heurística do texto
        if len(raw_text) < 50:
            category = 'Improdutivo'
            confidence = 0.55
            reason = 'Texto muito curto (<50 caracteres), provavelmente cumprimento (fallback - heurística)'
            matched_keywords = []
        else:
            category = 'Produtivo'
            confidence = 0.55
            reason = 'Texto longo, provavelmente requer ação (fallback - heurística)'
            matched_keywords = []
    
    return {
        'category': category,
        'reason': reason,
        'suggested_response': None,  # Não geramos resposta no fallback
        'confidence_score': confidence,
        'summary': reason,
        'used_fallback': True,
        'keyword_analysis': {
            'matched_keywords': matched_keywords,
            'produtivo_score': produtivo_score,
            'improdutivo_score': improdutivo_score,
            'total_keywords': len(keyword_list)
        }
    }


def should_use_full_text(raw_text: str, keywords: str) -> bool:
    """
    Decide se precisa enviar texto completo ou só keywords para IA.
    """
    # Se texto muito curto, keywords são suficientes
    if len(raw_text) < 100:
        return False
    
    # Se pré-classificação tem alta confiança, não precisa texto completo
    pre_classification = pre_classify_with_keywords(keywords)
    if pre_classification and pre_classification['confidence_score'] > 0.85:
        return False
    
    return True  # Precisa texto completo


def _analyze_with_ai(raw_text: str, nlp_keywords: str, use_full_text: bool = True) -> Dict[str, Any]:
    """
    Análise usando IA (Gemini).
    """
    client = _get_gemini_client()
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    
    # Otimizar prompt: usar texto completo ou apenas keywords
    if use_full_text:
        text_context = f"TEXTO ORIGINAL:\n{raw_text}\n\nCONTEXTO NLP (PALAVRAS-CHAVE PROCESSADAS):\n{nlp_keywords}"
    else:
        text_context = f"PALAVRAS-CHAVE EXTRAÍDAS DO EMAIL:\n{nlp_keywords}\n\n(Texto completo não disponível - use as palavras-chave para análise)"
    
    prompt = f"""Atue como um sistema de triagem de emails corporativos para uma empresa financeira.
Analise o seguinte email e retorne um JSON.

{text_context}

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
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        
        content = response.text.strip()
        
        # Limpar markdown se presente
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
        
        # Analisar keywords para incluir nos detalhes
        keyword_list = set(nlp_keywords.lower().split())
        matched_produtivo = keyword_list & PRODUTIVO_KEYWORDS
        matched_improdutivo = keyword_list & IMPRODUTIVO_KEYWORDS
        
        return {
            'category': categoria,
            'reason': razao,
            'suggested_response': sugestao_resposta if sugestao_resposta else None,
            'confidence_score': confidence_score,
            'summary': summary,
            'used_ai': True,
            'used_full_text': use_full_text,
            'keyword_analysis': {
                'matched_keywords': sorted(list(matched_produtivo | matched_improdutivo)),
                'produtivo_score': len(matched_produtivo),
                'improdutivo_score': len(matched_improdutivo),
                'total_keywords': len(keyword_list)
            }
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


def analyze_email(raw_text: str, nlp_keywords: str) -> Dict[str, Any]:
    # Passo 1: Tentar pré-classificação com keywords
    pre_classification = pre_classify_with_keywords(nlp_keywords)
    
    if pre_classification and pre_classification.get('confidence_score', 0) > 0.85:
        logger.info("Classificação feita apenas com keywords (alta confiança)")
        # Ainda precisamos da IA para gerar resposta se for produtivo
        if pre_classification['category'] == 'Produtivo':
            try:
                # Usar IA apenas para gerar resposta
                ai_result = _analyze_with_ai(raw_text, nlp_keywords, use_full_text=True)
                pre_classification['suggested_response'] = ai_result.get('suggested_response')
                pre_classification['used_ai'] = True
                # Manter keyword_analysis da pré-classificação
            except Exception as e:
                logger.warning(f"IA falhou ao gerar resposta, mas classificação já feita: {str(e)}")
                pre_classification['suggested_response'] = None
                pre_classification['used_ai'] = False
        
        return pre_classification
    
    # Passo 2: Usar IA para classificação
    try:
        use_full_text = should_use_full_text(raw_text, nlp_keywords)
        result = _analyze_with_ai(raw_text, nlp_keywords, use_full_text=use_full_text)
        logger.info(f"Classificação feita com IA (usou texto completo: {use_full_text})")
        return result
    
    except AIAPIException as e:
        logger.warning(f"IA falhou, usando fallback baseado em keywords: {str(e)}")
        # Passo 3: Fallback baseado em keywords
        return analyze_with_keywords_fallback(nlp_keywords, raw_text)


def _calculate_confidence_score(categoria: str, razao: str) -> float:
    base_score = 0.85
    
    if len(razao) > 20:
        base_score += 0.05
    
    if categoria == 'Produtivo' and 'solicit' in razao.lower():
        base_score += 0.05
    elif categoria == 'Improdutivo' and any(word in razao.lower() for word in ['felicitaç', 'agradec', 'cumpriment']):
        base_score += 0.05
    
    return min(base_score, 0.99)
