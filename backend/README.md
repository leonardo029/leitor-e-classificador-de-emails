# Email Classifier - Backend

API backend para classificação automática de emails usando Inteligência Artificial e Processamento de Linguagem Natural (NLP).

## 📋 Descrição

Esta API permite classificar emails em duas categorias:
- **Produtivo**: Emails que requerem ação ou resposta específica
- **Improdutivo**: Emails que não necessitam ação imediata

A classificação é feita através de:
1. Pré-processamento NLP usando NLTK (stopwords, stemming)
2. Análise com Google Gemini para classificação e geração de resposta sugerida

## 🚀 Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **NLTK**: Processamento de linguagem natural
- **Google Gemini API**: Classificação e geração de respostas
- **Pydantic**: Validação de dados
- **Docker**: Containerização

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

5. Configure as variáveis de ambiente:
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
    "suggested_response": "Prezado cliente, segue em anexo...",
    "nlp_debug": {
      "detected_keywords": "solicit segund via bolet"
    }
  }
}
```

### POST /api/v1/process-text

Processa um email via texto direto em JSON.

**Request:**
```json
{
  "text": "Prezado, gostaria de solicitar a segunda via do boleto..."
}
```

**Resposta:** Igual ao endpoint `/api/v1/process`

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
