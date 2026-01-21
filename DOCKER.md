# 🐳 Guia Docker - Email Classifier

Este projeto utiliza Docker Compose para executar frontend e backend juntos de forma simplificada.

## 📋 Pré-requisitos

- Docker instalado
- Docker Compose instalado (geralmente vem com Docker Desktop)

## 🚀 Como Usar

### 1. Configure as variáveis de ambiente

Crie um arquivo `.env` (ou copie o `.env.example`) na raiz do projeto com as seguintes variáveis:

```env
#Backend
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-3-flash-preview
GEMINI_TIMEOUT=30
MAX_FILE_SIZE_MB=10
MAX_TEXT_LENGTH=50000
CORS_ORIGINS=*

#Frontend
VITE_API_URL=http://localhost:8000
BACKEND_HOST=backend
BACKEND_PORT=8000
```

**Importante:** Substitua `sua_chave_aqui` pela sua chave real da API Google Gemini.  
**Obs:** Caso aponte o erro de que os arquivos `docker-entrypoint.sh` não estão sendo encotrados, altere a formatação dos arquivos de **CRLF** para **LF**.

### 2. Execute o Docker Compose

Na raiz do projeto, execute:

```bash
docker-compose up --build
```

Ou para executar em background:

```bash
docker-compose up -d --build
```

### 3. Acesse a aplicação

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## 🔧 Comandos Úteis

### Parar os serviços
```bash
docker-compose down
```

### Ver logs
```bash
docker-compose logs -f
```

### Ver logs de um serviço específico
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Reconstruir os containers
```bash
docker-compose up --build
```

### Parar e remover volumes
```bash
docker-compose down -v
```
