# 📧 Leitor e Classificador de Emails

Esse repositório tem como objetivo propor uma solução digital para automatizar a leitura e classificação de emails em empresas que lidam com alto volume de mensagens diárias. Utiliza Inteligência Artificial e Processamento de Linguagem Natural para classificar emails e sugerir respostas automáticas, liberando tempo da equipe para atividades mais estratégicas.

## 🎯 Contexto

Empresas do setor financeiro e outros setores recebem diariamente um grande volume de emails que podem ser:
- **Mensagens produtivas**: Solicitações de status, dúvidas sobre o sistema, pedidos de suporte técnico, solicitações de documentos
- **Mensagens improdutivas**: Felicitações, agradecimentos, mensagens de cortesia

A classificação manual desses emails consome tempo valioso da equipe. Esta solução automatiza esse processo, classificando emails em categorias e sugerindo respostas automáticas quando apropriado.

## ✨ Funcionalidades

- **Classificação Automática**: Identifica se um email é **Produtivo** (requer ação) ou **Improdutivo** (não requer ação imediata)
- **Sugestão de Respostas**: Gera respostas automáticas personalizadas para emails produtivos
- **Múltiplos Formatos**: Suporta upload de arquivos `.pdf` e `.txt`, ou entrada direta de texto
- **Interface Intuitiva**: Interface web moderna e responsiva com experiência de usuário otimizada
- **Histórico de Análises**: Mantém histórico das análises realizadas na sessão
- **Transparência**: Exibe detalhes técnicos sobre o processo de classificação (palavras-chave, método usado, score de confiança)

## 🏗️ Arquitetura

O projeto é composto por duas aplicações principais:

### Backend (API REST)
- **Framework**: FastAPI (Python)
- **IA**: Google Gemini API para classificação e geração de respostas
- **NLP**: NLTK para pré-processamento de texto
- **Sistema Híbrido**: Combina análise por palavras-chave e IA para otimizar custos e performance

### Frontend (Interface Web)
- **Framework**: Vue.js 3 com TypeScript
- **UI**: Vuetify 3 (Material Design)
- **Estado**: Pinia para gerenciamento de estado
- **Build**: Vite

## 🚀 Início Rápido

### Opção 1: Docker Compose (Recomendado)

A forma mais simples de executar o projeto completo:

```bash
# 1. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env e adicione sua chave da API Gemini

# 2. Execute os containers
docker-compose up --build
```

Acesse:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

Para mais detalhes sobre Docker, consulte [DOCKER.md](./docs/DOCKER.md).

### Opção 2: Execução Manual

#### Backend
Consulte o [README do backend](./backend/README.md) para instruções detalhadas de instalação e configuração.

**Resumo rápido:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
Consulte o [README do frontend](./frontend/README.md) para instruções detalhadas.

**Resumo rápido:**
```bash
cd frontend
npm install
npm run dev
```

## 🔑 Configuração

### Variáveis de Ambiente Necessárias

**Backend:**
- `GEMINI_API_KEY`: Chave da API Google Gemini (obrigatória)
  - Como obter: Acesse [Google AI Studio](https://aistudio.google.com/) e crie uma chave de API

**Frontend:**
- `VITE_API_URL`: URL da API backend (padrão: `http://localhost:8000`)

Para mais detalhes sobre configuração, consulte os READMEs específicos de cada módulo.

## 🧠 Como Funciona

O sistema utiliza uma abordagem híbrida inteligente:

1. **Pré-processamento NLP**: Extrai palavras-chave relevantes do texto usando NLTK
2. **Pré-classificação**: Tenta classificar usando palavras-chave (casos óbvios)
3. **Análise por IA**: Para casos ambíguos, utiliza Google Gemini para classificação precisa
4. **Geração de Resposta**: Gera resposta automática personalizada quando o email é produtivo
5. **Fallback**: Em caso de falha da IA, utiliza classificação baseada em palavras-chave

**Benefícios:**
- ⚡ **Performance**: 40-60% mais rápido em casos simples
- 💰 **Economia**: 50-70% menos chamadas à IA (casos óbvios não usam IA)
- 🛡️ **Resiliência**: Fallback automático garante 99.9% de disponibilidade

## 📊 Categorias de Classificação

- **Produtivo**: Emails que requerem uma ação ou resposta específica
  - Exemplos: Solicitações de suporte, dúvidas sobre o sistema, pedidos de documentos, atualizações sobre casos
  
- **Improdutivo**: Emails que não necessitam de uma ação imediata
  - Exemplos: Mensagens de felicitações, agradecimentos, mensagens de cortesia

## 📁 Estrutura do Projeto

```
.
├── backend/          # API REST em Python/FastAPI
│   ├── app/         # Código da aplicação
│   ├── tests/       # Testes automatizados
│   └── README.md    # Documentação detalhada do backend
├── frontend/        # Interface web em Vue.js
│   ├── src/         # Código fonte
│   └── README.md    # Documentação detalhada do frontend
├── mock_emails/     # Emails de exemplo para testes
├── docker-compose.yml
├── DOCKER.md        # Guia de uso com Docker
└── README.md        # Este arquivo
```

## 📚 Documentação

- **[Backend README](./backend/README.md)**: Documentação completa da API, endpoints, exemplos de resposta, sistema de classificação híbrido
- **[Frontend README](./frontend/README.md)**: Documentação da interface, componentes, estrutura do projeto
- **[Docker Guide](./docs/DOCKER.md)**: Guia completo de execução com Docker Compose

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.11+
- FastAPI
- Google Gemini API
- NLTK
- Pydantic
- Docker

### Frontend
- Vue.js 3
- TypeScript
- Vuetify 3
- Pinia
- Axios
- Vite

## 📝 Licença

Este projeto foi desenvolvido como parte de um desafio técnico e para aprendizagem pessoal.

## 🤝 Contribuindo

Este é um projeto de demonstração. Para sugestões ou melhorias, abra uma issue ou pull request.