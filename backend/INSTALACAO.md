# 📥 Guia de Instalação - Backend

Este guia explica passo a passo o que você precisa instalar localmente para executar o backend.

## ✅ Pré-requisitos

### 1. Python 3.11 ou superior

**Como verificar se você tem Python instalado:**
```bash
python --version
```

**Se não tiver Python instalado:**
- **Windows**: Baixe em [python.org](https://www.python.org/downloads/)
  - ⚠️ **Importante**: Durante a instalação, marque a opção "Add Python to PATH"
  
- **Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

- **MacOS**:
```bash
brew install python@3.11
```

### 2. pip (gerenciador de pacotes Python)

Geralmente vem instalado com o Python. Para verificar:
```bash
pip --version (em versões antigas)
python -m pip --version (em versões mais novas)
```

Se não estiver instalado:
```bash
python -m ensurepip --upgrade
```

### 3. Chave da API Google Gemini

Você precisa de uma chave da API Google Gemini para usar o serviço de classificação:
1. Acesse [aistudio.google.com](https://aistudio.google.com/)
2. Faça login com sua conta Google
3. Vá em "Get API Key" e crie uma nova chave
4. Copie a chave (ela será exibida apenas uma vez)

---

## 🚀 Instalação Passo a Passo

### Passo 1: Navegue até a pasta backend

```bash
cd backend
```

### Passo 2: Crie um ambiente virtual (recomendado)

Isola as dependências do projeto:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Você saberá que o ambiente virtual está ativo quando aparecer `(venv)` no início da linha do terminal.

### Passo 3: Instale as dependências

```bash
pip install -r requirements.txt
```

**O que será instalado:**
- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `python-multipart` - Suporte para upload de arquivos
- `pydantic` - Validação de dados
- `google-generativeai` - Cliente da API Google Gemini
- `pypdf` - Leitura de arquivos PDF
- `nltk` - Processamento de linguagem natural
- `python-dotenv` - Gerenciamento de variáveis de ambiente
- `slowapi` - Rate limiting

⏱️ **Tempo estimado**: 1-3 minutos (dependendo da conexão)

### Passo 4: Baixe os dados do NLTK

O NLTK precisa baixar alguns dados (stopwords, tokenizadores, etc). Isso acontece automaticamente na primeira execução, mas você pode fazer manualmente:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('rslp')"
```

⏱️ **Tempo estimado**: 30 segundos

### Passo 5: Configure as variáveis de ambiente

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da API Google Gemini:
```
GEMINI_API_KEY=sua-chave-aqui
```

⚠️ **Nunca compartilhe ou faça commit da chave da API!**

---

## ✅ Verificação da Instalação

Execute este comando para verificar se tudo está instalado corretamente:

```bash
python -c "import fastapi, uvicorn, nltk, google.generativeai; print('✅ Todas as dependências instaladas!')"
```

Se aparecer a mensagem de sucesso, está tudo pronto!

---

## 🏃 Executando o Backend

Após completar a instalação, execute:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Você verá uma mensagem como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

Acesse:
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🐳 Alternativa: Usar Docker (Opcional)

Se você tem Docker instalado, não precisa instalar Python localmente:

```bash
docker build -t email-classifier-api .
docker run -p 8000:8000 --env-file .env email-classifier-api
```

**Para instalar Docker:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac)
- [Docker Engine](https://docs.docker.com/engine/install/) (Linux)

---

## ❓ Problemas Comuns

### "python não é reconhecido como comando"
- **Solução**: Adicione Python ao PATH ou use `python3` em vez de `python`

### "pip não é reconhecido"
- **Solução**: Execute `python -m ensurepip --upgrade`

### "Erro ao baixar dados do NLTK"
- **Solução**: Execute manualmente o comando do Passo 4

### "ModuleNotFoundError"
- **Solução**: Certifique-se de que o ambiente virtual está ativo e execute `pip install -r requirements.txt` novamente

### "GEMINI_API_KEY não configurada"
- **Solução**: Verifique se o arquivo `.env` existe e contém a chave correta

---

## 📝 Resumo Rápido

```bash
# 1. Navegar para a pasta
cd backend

# 2. Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar .env
cp .env.example .env
# Editar .env e adicionar GEMINI_API_KEY

# 5. Executar
uvicorn app.main:app --reload
```

---

Pronto! Seu backend está configurado e pronto para uso! 🎉
