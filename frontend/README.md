# Email Classifier - Frontend

Frontend web para classificação automática de emails usando Vue.js 3, TypeScript, Vuetify 3 e Pinia.

## 🚀 Tecnologias

- **Vue 3**: Framework JavaScript progressivo
- **TypeScript**: Tipagem estática
- **Vuetify 3**: Framework de componentes Material Design
- **Pinia**: Gerenciamento de estado
- **Axios**: Cliente HTTP
- **Vite**: Build tool moderna e rápida

## 📦 Instalação

### Pré-requisitos

- Node.js 18+ e npm

### Passo a Passo

1. Instale as dependências:
```bash
npm install
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure a URL da API:
```
VITE_API_URL=http://localhost:8000
```

3. Execute em modo desenvolvimento:
```bash
npm run dev
```

A aplicação estará disponível em: `http://localhost:5173`

## 🔧 Scripts Disponíveis

- `npm run dev`: Inicia servidor de desenvolvimento
- `npm run build`: Build para produção
- `npm run preview`: Preview do build de produção

## 📁 Estrutura do Projeto

```
frontend/
├── src/
│   ├── components/       # Componentes Vue
│   │   ├── AppHeader.vue
│   │   ├── AnalysisForm.vue
│   │   └── ResultList.vue
│   ├── interfaces/       # Interfaces TypeScript
│   │   └── IAnalysis.ts
│   ├── stores/          # Stores Pinia
│   │   └── analysisStore.ts
│   ├── services/        # Serviços
│   │   └── api.ts
│   ├── App.vue          # Componente raiz
│   └── main.ts          # Entrypoint
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## 🎨 Funcionalidades

- Upload de arquivos PDF/TXT
- Entrada de texto direto (até 50.000 caracteres)
- Classificação automática (Produtivo/Improdutivo)
- Sugestão de resposta automática
- Histórico persistido em sessionStorage
- Sistema de cores baseado em score (semáforo)
- Detalhes técnicos NLP (expand/collapse)
- Validações de entrada no frontend

## 🔌 Integração com Backend

A aplicação se conecta com a API backend através dos seguintes endpoints:

- `POST /api/v1/process`: Processa arquivo ou texto via form-data
- `POST /api/v1/process-text`: Processa texto direto via JSON

## 📝 Licença

Este projeto foi desenvolvido para o desafio da AutoU.
