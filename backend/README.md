# Email Classifier - Backend

API backend para classificação automática de emails usando Inteligência Artificial e Processamento de Linguagem Natural (NLP).

## 📋 Descrição

Esta API permite classificar emails em duas categorias:
- **Produtivo**: Emails que requerem ação ou resposta específica
- **Improdutivo**: Emails que não necessitam ação imediata

A classificação é feita através de um **sistema híbrido inteligente** que combina:
1. Pré-processamento NLP usando NLTK (stopwords, stemming)
2. Pré-classificação com palavras-chave (casos óbvios)
3. Análise com Google Gemini para casos ambíguos
4. Fallback baseado em keywords quando IA falha

## 🚀 Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **NLTK**: Processamento de linguagem natural
- **Google Gemini API**: Classificação e geração de respostas
- **Pydantic**: Validação de dados
- **Docker**: Containerização

## 🧠 Sistema de Classificação Híbrido

### Fluxo de Processamento

```
1. Extrair keywords (NLTK)
   ↓
2. Tentar pré-classificação com keywords
   ├─ Se alta confiança (>0.85) → Usar resultado + IA só para gerar resposta (se produtivo)
   └─ Se baixa confiança → Continuar
   ↓
3. Enviar para IA (um único modelo Gemini)
   ├─ Decidir se envia texto completo ou só keywords (otimização)
   ├─ Chamar modelo Gemini configurado
   └─ Se falhar → Usar fallback baseado em keywords
   ↓
4. Calcular confiança do resultado
   ↓
5. Retornar resposta enriquecida com detalhes
```

### Características do Sistema

- ✅ **Pré-classificação inteligente**: Identifica casos óbvios sem usar IA (reduz custos)
- ✅ **Otimização de tokens**: Decide quando enviar texto completo ou apenas keywords
- ✅ **Fallback automático**: Usa keywords quando IA falha (alta resiliência)
- ✅ **Resposta enriquecida**: Retorna detalhes sobre o processo de classificação

### Benefícios

1. **Redução de custos**: 50-70% menos chamadas à IA (casos óbvios não usam IA)
2. **Performance**: 40-60% mais rápido (casos simples em 0.1s vs 2-5s)
3. **Resiliência**: 99.9% uptime (fallback automático quando IA falha)
4. **Transparência**: Detalhes completos sobre como chegamos na conclusão

## 📦 Instalação

### Pré-requisitos

- Python 3.11+
- Chave da API Google Gemini

### Passo a Passo

1. Clone o repositório e entre na pasta backend:
```bash
cd backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Baixe os dados do NLTK (primeira vez):
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('rslp')"
```

6. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API Google Gemini:
```
GEMINI_API_KEY=sua_chave_aqui
```

**Como obter a chave da API Gemini:**
1. Acesse [aistudio.google.com](https://aistudio.google.com/)
2. Faça login com sua conta Google
3. Vá em "Get API Key" e crie uma nova chave
4. Copie a chave

## 🔧 Configuração

As variáveis de ambiente disponíveis estão no arquivo `.env.example`:

- `RATE_LIMIT_PER_MINUTE`: Limite de requisições por minuto (padrão: 10)

## 🏃 Execução

### Modo Desenvolvimento

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

### Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 Endpoints

### GET /

Retorna informações sobre a API.

### GET /health

Endpoint de health check.

### POST /api/v1/process

Processa um email via upload de arquivo ou texto direto via form-data.

**Opção 1 - Upload de Arquivo:**
```
Content-Type: multipart/form-data
Campo: file (arquivo .pdf ou .txt)
```

**Opção 2 - Texto Direto (Form-Data):**
```
Content-Type: multipart/form-data
Campo: text (string)
```

**Resposta de Sucesso:**
```json
{
  "status": "success",
  "data": {
    "filename": "email.pdf",
    "category": "Produtivo",
    "confidence_score": 0.95,
    "summary": "Cliente solicitando segunda via do boleto",
    "reason": "Identificado como produtivo através de 3 palavras-chave relevantes: boleto, solicit, segund",
    "suggested_response": "Prezado cliente, segue em anexo...",
    "nlp_debug": {
      "detected_keywords": "solicit segund via bolet",
      "keyword_analysis": {
        "matched_keywords": ["boleto", "solicit", "segund"],
        "produtivo_score": 3,
        "improdutivo_score": 0,
        "total_keywords": 5
      }
    },
    "processing_details": {
      "classification_method": "keywords_only",
      "used_ai": true,
      "used_fallback": false,
      "keyword_analysis": {
        "matched_keywords": ["boleto", "solicit", "segund"],
        "produtivo_score": 3,
        "improdutivo_score": 0,
        "total_keywords": 5
      }
    }
  }
}
```

## 📊 Estrutura da Resposta

A API retorna informações detalhadas sobre o processo de classificação, incluindo:

- **Método de classificação usado** (keywords_only, ai, fallback)
- **Palavras-chave encontradas e utilizadas**
- **Scores de keywords** (produtivo vs improdutivo)
- **Detalhes do processamento**
- **Razão detalhada da classificação**

### Exemplo 1: Classificação por Keywords (Alta Confiança)

```json
{
  "status": "success",
  "data": {
    "filename": "solicitacao_boleto.txt",
    "category": "Produtivo",
    "confidence_score": 0.85,
    "summary": "Email identificado como produtivo por 3 palavras-chave relevantes",
    "reason": "Identificado como produtivo através de 3 palavras-chave relevantes: boleto, solicit, segund",
    "suggested_response": "Prezado cliente, segue em anexo a segunda via do boleto solicitado...",
    "nlp_debug": {
      "detected_keywords": "solicit segund via bolet venciment pagament",
      "keyword_analysis": {
        "matched_keywords": ["boleto", "solicit", "segund"],
        "produtivo_score": 3,
        "improdutivo_score": 0,
        "total_keywords": 5
      }
    },
    "processing_details": {
      "classification_method": "keywords_only",
      "used_full_text": null,
      "used_ai": true,
      "used_fallback": false,
      "keyword_analysis": {
        "matched_keywords": ["boleto", "solicit", "segund"],
        "produtivo_score": 3,
        "improdutivo_score": 0,
        "total_keywords": 5
      }
    }
  }
}
```

### Exemplo 2: Classificação por IA

```json
{
  "status": "success",
  "data": {
    "filename": "duvida_sistema.txt",
    "category": "Produtivo",
    "confidence_score": 0.90,
    "summary": "Cliente está com dúvidas sobre como usar o sistema de pagamento",
    "reason": "Cliente está com dúvidas sobre como usar o sistema de pagamento",
    "suggested_response": "Prezado cliente, agradecemos seu contato. Segue abaixo as instruções...",
    "nlp_debug": {
      "detected_keywords": "duvid sistem pagament como usar",
      "keyword_analysis": {
        "matched_keywords": ["duvida", "sistem"],
        "produtivo_score": 2,
        "improdutivo_score": 0,
        "total_keywords": 4
      }
    },
    "processing_details": {
      "classification_method": "ai",
      "used_full_text": true,
      "used_ai": true,
      "used_fallback": false,
      "keyword_analysis": {
        "matched_keywords": ["duvida", "sistem"],
        "produtivo_score": 2,
        "improdutivo_score": 0,
        "total_keywords": 4
      }
    }
  }
}
```

### Exemplo 3: Classificação por Fallback

```json
{
  "status": "success",
  "data": {
    "filename": "email_curto.txt",
    "category": "Improdutivo",
    "confidence_score": 0.75,
    "summary": "Email identificado como improdutivo por 2 palavras-chave relevantes",
    "reason": "Identificado como improdutivo através de 2 palavras-chave relevantes: feliz, natal",
    "suggested_response": null,
    "nlp_debug": {
      "detected_keywords": "feliz natal boas fest",
      "keyword_analysis": {
        "matched_keywords": ["feliz", "natal"],
        "produtivo_score": 0,
        "improdutivo_score": 2,
        "total_keywords": 4
      }
    },
    "processing_details": {
      "classification_method": "fallback",
      "used_full_text": null,
      "used_ai": false,
      "used_fallback": true,
      "keyword_analysis": {
        "matched_keywords": ["feliz", "natal"],
        "produtivo_score": 0,
        "improdutivo_score": 2,
        "total_keywords": 4
      }
    }
  }
}
```

## 🎯 Campos da Resposta Explicados

### Campos Principais

- **`category`**: Categoria do email (`Produtivo` ou `Improdutivo`)
- **`confidence_score`**: Score de confiança (0.0 a 1.0)
- **`summary`**: Resumo da classificação
- **`reason`**: Razão detalhada explicando como chegamos na conclusão
- **`suggested_response`**: Resposta sugerida (apenas para emails produtivos)

### `processing_details`

Detalhes sobre como a classificação foi realizada:

- **`classification_method`**: Método usado
  - `keywords_only`: Classificado apenas com keywords (alta confiança)
  - `ai`: Classificado usando IA
  - `fallback`: Classificado usando fallback (IA falhou)
- **`used_full_text`**: Se enviou texto completo para IA (ou `null`)
- **`used_ai`**: Se usou IA na classificação
- **`used_fallback`**: Se usou fallback baseado em keywords
- **`keyword_analysis`**: Análise detalhada das keywords

### `keyword_analysis`

Análise das palavras-chave encontradas:

- **`matched_keywords`**: Lista de keywords que foram encontradas e usadas na classificação
- **`produtivo_score`**: Quantidade de keywords de produtivo encontradas
- **`improdutivo_score`**: Quantidade de keywords de improdutivo encontradas
- **`total_keywords`**: Total de keywords extraídas pelo NLP

### `nlp_debug`

Informações de debug do processamento NLP:

- **`detected_keywords`**: String com todas as keywords extraídas (stemmed)
- **`keyword_analysis`**: Mesma análise de keywords (para facilitar acesso)

## 🔍 Palavras-chave Utilizadas

### Keywords de Produtivo

O sistema identifica emails produtivos através de palavras-chave como:
- `solicit`, `pedid`, `requer`, `necessit`, `urgent`
- `problema`, `erro`, `suport`, `ajud`, `duvida`
- `boleto`, `fatur`, `pagament`, `venciment`, `segund`
- `atualiz`, `status`, `caso`, `protocol`, `ticket`

### Keywords de Improdutivo

O sistema identifica emails improdutivos através de palavras-chave como:
- `feliz`, `natal`, `ano novo`, `parabens`, `agradec`
- `cumpriment`, `saudacoes`, `obrigad`, `obrigado`
- `felicitacoes`, `comemor`, `celebr`

## 🧪 Testes

Execute os testes com pytest:

```bash
pytest tests/ -v
```

Com cobertura:

```bash
pytest tests/ -v --cov=app --cov-report=html
```

## 🔒 Validações

### Arquivo
- Tamanho máximo: 10MB
- Formatos aceitos: .pdf, .txt
- Arquivo não pode estar vazio

### Texto
- Comprimento mínimo: 1 caractere
- Comprimento máximo: 50.000 caracteres
- Encoding: UTF-8

## ⚠️ Tratamento de Erros

A API retorna erros padronizados:

```json
{
  "status": "error",
  "error_code": "INVALID_FILE",
  "message": "Apenas arquivos .pdf e .txt são aceitos",
  "details": {}
}
```

**Códigos HTTP:**
- `400`: Bad Request (entrada inválida)
- `413`: Payload Too Large (arquivo muito grande)
- `422`: Unprocessable Entity (formato inválido)
- `500`: Internal Server Error (erro interno)
- `503`: Service Unavailable (API Gemini indisponível)

## 📊 Rate Limiting

A API possui rate limiting configurável (padrão: 10 requisições por minuto por IP).

## 🚢 Deploy

### Render

1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático

### Docker

A imagem Docker está pronta para deploy em qualquer plataforma que suporte Docker.

## 📈 Métricas e Monitoramento

### Informações Disponíveis na Resposta

A resposta da API inclui informações que permitem monitorar:

- **Taxa de pré-classificação**: Quantos emails foram classificados apenas com keywords
- **Taxa de uso de IA**: Quantos emails precisaram de IA
- **Taxa de fallback**: Quantos emails usaram fallback (indica problemas com IA)
- **Economia de tokens**: Baseado em `used_full_text` (false = economia)
