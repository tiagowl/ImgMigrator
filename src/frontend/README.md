# Cloud Migrate Frontend

Frontend do sistema de migração de fotos do iCloud para Google Drive.

## Tecnologias

- **React 18** - Framework UI
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router** - Roteamento
- **Zustand** - Gerenciamento de estado
- **Axios** - Cliente HTTP
- **Socket.io** - WebSocket para progresso em tempo real
- **React Hook Form** - Formulários
- **Zod** - Validação
- **Tailwind CSS** - Estilização
- **React Hot Toast** - Notificações

## Estrutura do Projeto

```
src/
├── components/     # Componentes reutilizáveis
├── pages/         # Páginas da aplicação
├── services/      # Serviços de API
├── hooks/         # Hooks customizados
├── store/         # Estado global (Zustand)
├── types/         # Tipos TypeScript
├── utils/         # Funções utilitárias
└── styles/        # Estilos globais
```

## Instalação

```bash
npm install
```

## Desenvolvimento

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`

## Build

```bash
npm run build
```

## Variáveis de Ambiente

Copie o arquivo de exemplo e configure as variáveis:

```bash
cp env.example .env.local
```

Edite `.env.local` com suas configurações:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Scripts Disponíveis

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run preview` - Preview do build de produção
- `npm run lint` - Executa linter
- `npm run type-check` - Verifica tipos TypeScript

