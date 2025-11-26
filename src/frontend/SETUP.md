# Guia de Setup - Frontend

## Instalação

1. **Instalar dependências:**
```bash
cd src/frontend
npm install
```

2. **Configurar variáveis de ambiente:**
```bash
cp .env.example .env.local
```

Edite `.env.local` com suas configurações:
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

3. **Iniciar servidor de desenvolvimento:**
```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`

## Estrutura do Projeto

```
src/
├── components/          # Componentes reutilizáveis
│   ├── Button/
│   ├── Card/
│   ├── Input/
│   ├── Layout/
│   ├── LoadingSpinner/
│   ├── ProgressBar/
│   └── StatusBadge/
├── pages/              # Páginas da aplicação
│   ├── Dashboard/
│   ├── History/
│   ├── Settings/
│   └── MigrationDetail/
├── services/           # Serviços de API
│   ├── api.ts
│   ├── authService.ts
│   ├── credentialService.ts
│   └── migrationService.ts
├── store/              # Estado global (Zustand)
│   ├── useAuthStore.ts
│   ├── useCredentialStore.ts
│   └── useMigrationStore.ts
├── hooks/              # Hooks customizados
│   ├── usePolling.ts
│   └── useWebSocket.ts
├── types/              # Tipos TypeScript
│   └── index.ts
├── utils/              # Funções utilitárias
│   ├── constants.ts
│   ├── formatters.ts
│   └── cn.ts
└── styles/             # Estilos globais
    └── index.css
```

## Funcionalidades Implementadas

### ✅ Componentes Base
- Button (primário, secundário, danger)
- Input (com validação e estados de erro)
- Card
- ProgressBar
- LoadingSpinner
- StatusBadge

### ✅ Páginas
- **Dashboard**: Visualização de status, credenciais e migrações ativas
- **Settings**: Configuração de credenciais (Google Drive e iCloud)
- **History**: Histórico de todas as migrações
- **MigrationDetail**: Detalhes e progresso de uma migração específica

### ✅ Serviços
- Integração completa com API backend
- Tratamento de erros
- Interceptors para autenticação
- Notificações toast

### ✅ Estado Global
- Gerenciamento de autenticação
- Gerenciamento de credenciais
- Gerenciamento de migrações

### ✅ Hooks Customizados
- `usePolling`: Atualização periódica de dados
- `useWebSocket`: Conexão WebSocket para progresso em tempo real

## Design System

O frontend implementa o Design System definido nos documentos UX:

- **Cores**: Paleta completa (primário, sucesso, erro, aviso, neutros)
- **Tipografia**: Escala tipográfica definida
- **Espaçamento**: Sistema baseado em 4px
- **Componentes**: Seguindo padrões de acessibilidade (WCAG AA)
- **Responsividade**: Mobile-first, breakpoints definidos

## Próximos Passos

1. Instalar dependências: `npm install`
2. Configurar variáveis de ambiente
3. Iniciar backend em `http://localhost:8000`
4. Iniciar frontend: `npm run dev`
5. Acessar `http://localhost:3000`

## Notas

- O erro de tipo do `zustand` será resolvido após `npm install`
- Certifique-se de que o backend está rodando antes de iniciar o frontend
- Para produção, configure as variáveis de ambiente adequadamente






