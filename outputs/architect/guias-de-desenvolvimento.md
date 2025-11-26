# Guias de Desenvolvimento - Sistema de Migração iCloud para Google Drive

## 1. Configuração do Ambiente de Desenvolvimento

### 1.1 Pré-requisitos

**Software Necessário:**
- Python 3.11+
- Node.js 18+ e npm
- Docker e Docker Compose
- Git
- Editor de código (VS Code recomendado)

**Extensões VS Code Recomendadas:**
- Python
- Pylance
- ESLint
- Prettier
- Docker

### 1.2 Setup Inicial

**1. Clone o repositório:**
```bash
git clone https://github.com/org/cloud-migrate.git
cd cloud-migrate
```

**2. Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Frontend:**
```bash
cd frontend
npm install
```

**4. Variáveis de Ambiente:**
```bash
# Backend
cp .env.example .env
# Edite .env com suas configurações

# Frontend
cp .env.example .env.local
```

**5. Banco de Dados:**
```bash
cd backend
alembic upgrade head
```

**6. Iniciar com Docker Compose:**
```bash
docker-compose up -d
```

---

## 2. Convenções de Código

### 2.1 Python (Backend)

**Style Guide:** PEP 8

**Formatação:**
- Usar `black` para formatação automática
- Linha máxima: 100 caracteres
- Usar type hints em todas as funções

**Exemplo:**
```python
from typing import Optional
from pydantic import BaseModel

def get_user_by_id(user_id: int) -> Optional[User]:
    """Busca usuário por ID.
    
    Args:
        user_id: ID do usuário
        
    Returns:
        User se encontrado, None caso contrário
    """
    return db.query(User).filter(User.id == user_id).first()
```

**Nomenclatura:**
- Classes: `PascalCase` (ex: `UserRepository`)
- Funções/Métodos: `snake_case` (ex: `get_user_by_id`)
- Constantes: `UPPER_SNAKE_CASE` (ex: `MAX_RETRY_ATTEMPTS`)
- Variáveis: `snake_case` (ex: `user_email`)

**Imports:**
```python
# Ordem: stdlib, third-party, local
import os
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.user_service import UserService
```

### 2.2 TypeScript/React (Frontend)

**Style Guide:** Airbnb JavaScript Style Guide

**Formatação:**
- Usar Prettier com configuração padrão
- 2 espaços para indentação
- Aspas simples para strings

**Exemplo:**
```typescript
interface User {
  id: number;
  email: string;
  createdAt: string;
}

const getUserById = async (userId: number): Promise<User | null> => {
  try {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user:', error);
    return null;
  }
};
```

**Nomenclatura:**
- Componentes: `PascalCase` (ex: `UserDashboard`)
- Funções/Variáveis: `camelCase` (ex: `getUserById`)
- Constantes: `UPPER_SNAKE_CASE` (ex: `API_BASE_URL`)
- Arquivos: `kebab-case` (ex: `user-dashboard.tsx`)

**Componentes:**
```typescript
import React from 'react';

interface UserDashboardProps {
  userId: number;
  onUserUpdate?: (user: User) => void;
}

export const UserDashboard: React.FC<UserDashboardProps> = ({
  userId,
  onUserUpdate,
}) => {
  // Component logic
  return <div>User Dashboard</div>;
};
```

---

## 3. Estrutura de Commits

### 3.1 Formato

Usar Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (não afeta código)
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```
feat(auth): add OAuth Google Drive integration

Implement OAuth 2.0 flow for Google Drive authentication.
Includes token refresh and error handling.

Closes #123
```

```
fix(migration): retry failed photos on resume

When resuming a paused migration, photos that failed
are now retried automatically.

Fixes #456
```

---

## 4. Padrões de Desenvolvimento

### 4.1 Criação de Nova Feature

**1. Criar Branch:**
```bash
git checkout -b feat/nome-da-feature
```

**2. Desenvolver:**
- Escrever código
- Adicionar testes
- Atualizar documentação

**3. Commitar:**
```bash
git add .
git commit -m "feat(scope): description"
```

**4. Push e PR:**
```bash
git push origin feat/nome-da-feature
# Criar Pull Request no GitHub
```

### 4.2 Estrutura de uma Feature

**Backend:**
```
app/
├── api/routes/
│   └── nova_feature.py      # Rotas
├── models/
│   └── nova_feature.py      # Modelos SQLAlchemy
├── schemas/
│   └── nova_feature.py      # Schemas Pydantic
├── services/
│   └── nova_feature_service.py  # Lógica de negócio
└── repositories/
    └── nova_feature_repository.py  # Acesso a dados
```

**Frontend:**
```
src/
├── components/
│   └── NovaFeature/
│       ├── NovaFeature.tsx
│       └── NovaFeature.test.tsx
├── pages/
│   └── NovaFeaturePage.tsx
├── services/
│   └── novaFeatureService.ts
└── hooks/
    └── useNovaFeature.ts
```

### 4.3 Tratamento de Erros

**Backend:**
```python
from fastapi import HTTPException, status

def get_user(user_id: int) -> User:
    user = user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user
```

**Frontend:**
```typescript
try {
  const user = await userService.getUser(userId);
  setUser(user);
} catch (error) {
  if (error.response?.status === 404) {
    showError('Usuário não encontrado');
  } else {
    showError('Erro ao carregar usuário');
  }
}
```

---

## 5. Testes

### 5.1 Estrutura de Testes

**Backend:**
```
tests/
├── unit/
│   ├── test_services/
│   ├── test_repositories/
│   └── test_utils/
├── integration/
│   ├── test_api/
│   └── test_database/
└── e2e/
    └── test_migration_flow.py
```

**Frontend:**
```
src/
├── components/
│   └── Component/
│       └── Component.test.tsx
└── __tests__/
    └── integration/
```

### 5.2 Escrevendo Testes

**Backend (pytest):**
```python
import pytest
from app.services.user_service import UserService
from app.models.user import User

def test_get_user_by_id_success():
    # Arrange
    user_id = 1
    expected_user = User(id=1, email="test@example.com")
    
    # Act
    user = user_service.get_user_by_id(user_id)
    
    # Assert
    assert user is not None
    assert user.id == user_id
    assert user.email == "test@example.com"

def test_get_user_by_id_not_found():
    # Arrange
    user_id = 999
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user_by_id(user_id)
    
    assert exc_info.value.status_code == 404
```

**Frontend (Jest + React Testing Library):**
```typescript
import { render, screen } from '@testing-library/react';
import { UserDashboard } from './UserDashboard';

describe('UserDashboard', () => {
  it('renders user information', () => {
    const user = { id: 1, email: 'test@example.com' };
    
    render(<UserDashboard userId={user.id} />);
    
    expect(screen.getByText(user.email)).toBeInTheDocument();
  });
});
```

### 5.3 Executando Testes

**Backend:**
```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Teste específico
pytest tests/unit/test_services/test_user_service.py
```

**Frontend:**
```bash
# Todos os testes
npm test

# Com cobertura
npm test -- --coverage

# Watch mode
npm test -- --watch
```

---

## 6. Code Review

### 6.1 Checklist de Review

**Funcionalidade:**
- [ ] Código atende aos requisitos?
- [ ] Edge cases foram considerados?
- [ ] Tratamento de erros adequado?

**Qualidade:**
- [ ] Código segue convenções?
- [ ] Nomes descritivos?
- [ ] Sem código duplicado?
- [ ] Comentários quando necessário?

**Testes:**
- [ ] Testes unitários adicionados?
- [ ] Testes de integração (se aplicável)?
- [ ] Cobertura adequada (>80%)?

**Documentação:**
- [ ] Docstrings/comentários atualizados?
- [ ] README atualizado (se necessário)?
- [ ] Changelog atualizado?

**Segurança:**
- [ ] Inputs validados?
- [ ] Credenciais não expostas?
- [ ] SQL injection prevenido?

### 6.2 Processo de Review

1. **Criar PR:**
   - Descrição clara do que foi feito
   - Link para issue relacionada
   - Screenshots (se UI)

2. **Review:**
   - Pelo menos 1 aprovação necessária
   - Resolver comentários antes de merge

3. **Merge:**
   - Squash commits (se necessário)
   - Deletar branch após merge

---

## 7. Debugging

### 7.1 Backend

**Logs:**
```python
import logging

logger = logging.getLogger(__name__)

logger.info("Starting migration", extra={"migration_id": 1})
logger.error("Migration failed", exc_info=True)
```

**Debugger:**
```python
# VS Code: Adicionar breakpoint
# Ou usar pdb
import pdb; pdb.set_trace()
```

**Testar API:**
```bash
# Swagger UI
http://localhost:8000/docs

# Ou usar httpx/curl
curl http://localhost:8000/api/users/1
```

### 7.2 Frontend

**React DevTools:**
- Instalar extensão do browser
- Inspecionar componentes e estado

**Console:**
```typescript
console.log('Debug info:', { userId, data });
console.error('Error:', error);
```

**Network Tab:**
- Ver requisições HTTP
- Verificar payloads e respostas

---

## 8. Performance

### 8.1 Backend

**Profiling:**
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# Seu código aqui
profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

**Otimizações:**
- Usar async/await para I/O
- Connection pooling no banco
- Cache com Redis quando apropriado
- Lazy loading de relacionamentos

### 8.2 Frontend

**React DevTools Profiler:**
- Identificar componentes lentos
- Verificar re-renders desnecessários

**Otimizações:**
- `React.memo` para componentes puros
- `useMemo` e `useCallback` quando necessário
- Code splitting com lazy loading
- Otimizar imagens

---

## 9. Segurança

### 9.1 Boas Práticas

**Backend:**
- Sempre validar inputs
- Usar prepared statements (SQLAlchemy faz isso)
- Criptografar dados sensíveis
- Rate limiting em endpoints públicos
- Logs não devem conter dados sensíveis

**Frontend:**
- Não armazenar tokens em localStorage (usar httpOnly cookies se possível)
- Sanitizar inputs do usuário
- Validar no cliente E no servidor
- HTTPS sempre em produção

### 9.2 Checklist de Segurança

- [ ] Credenciais em variáveis de ambiente
- [ ] Inputs validados
- [ ] SQL injection prevenido
- [ ] XSS prevenido
- [ ] CSRF protection (se necessário)
- [ ] Rate limiting implementado
- [ ] Logs não expõem dados sensíveis
- [ ] HTTPS em produção

---

## 10. Deploy

### 10.1 Ambiente de Desenvolvimento

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev

# Worker
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

### 10.2 Ambiente de Staging

```bash
docker-compose -f docker-compose.staging.yml up -d
```

### 10.3 Ambiente de Produção

**Checklist:**
- [ ] Variáveis de ambiente configuradas
- [ ] SSL/TLS configurado
- [ ] Backup do banco configurado
- [ ] Monitoramento ativo
- [ ] Logs centralizados
- [ ] Health checks configurados

---

## 11. Troubleshooting

### 11.1 Problemas Comuns

**Backend não inicia:**
- Verificar variáveis de ambiente
- Verificar se porta está disponível
- Verificar logs de erro

**Migração não inicia:**
- Verificar se Redis está rodando
- Verificar se worker está ativo
- Verificar logs do Celery

**Erro de autenticação:**
- Verificar credenciais OAuth
- Verificar redirect URI
- Verificar tokens no banco

### 11.2 Logs

**Localizar logs:**
```bash
# Docker
docker-compose logs -f backend

# Aplicação
tail -f logs/app.log

# Celery
celery -A app.workers.celery_app events
```

---

## 12. Recursos Adicionais

### 12.1 Documentação

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Celery Docs](https://docs.celeryq.dev/)
- [React Docs](https://react.dev/)

### 12.2 Ferramentas Úteis

- **Postman/Insomnia:** Testar APIs
- **DB Browser for SQLite:** Visualizar banco
- **Redis Commander:** Visualizar Redis
- **Flower:** Monitorar Celery

---

**Documento gerado em:** [Data atual]  
**Versão:** 1.0  
**Status:** Guia de desenvolvimento completo






