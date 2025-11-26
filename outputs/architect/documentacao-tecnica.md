# Documentação Técnica - Sistema de Migração iCloud para Google Drive

## 1. Visão Geral do Sistema

### 1.1 Descrição

Sistema fullstack em Python para migração automatizada de fotos do iCloud para Google Drive. A aplicação permite que usuários configurem credenciais, iniciem migrações e acompanhem o progresso em tempo real através de uma interface web.

### 1.2 Objetivos Técnicos

- **Performance:** Processamento assíncrono de migrações
- **Segurança:** Criptografia de credenciais (AES-256)
- **Escalabilidade:** Arquitetura preparada para múltiplos workers
- **Confiabilidade:** Retry automático e recuperação de falhas
- **Manutenibilidade:** Código limpo e bem documentado

---

## 2. Stack Tecnológica

### 2.1 Backend

**Framework Web:**
- **FastAPI** 0.104+
  - Performance superior ao Flask
  - Suporte nativo a async/await
  - Documentação automática (OpenAPI/Swagger)
  - Validação de dados com Pydantic

**ORM e Banco de Dados:**
- **SQLAlchemy** 2.0+
  - ORM moderno e type-safe
  - Migrations com Alembic
  - Suporte a async

- **SQLite** 3.40+
  - Banco de dados embutido
  - Adequado para MVP e pequena escala
  - WAL mode para melhor concorrência

**Processamento Assíncrono:**
- **Celery** 5.3+ com **Redis**
  - Background jobs para migrações
  - Fila de tarefas distribuída
  - Retry automático
  - Monitoramento com Flower

**Autenticação:**
- **Authlib** 1.2+
  - OAuth 2.0 client
  - Integração com Google Drive API

**Criptografia:**
- **cryptography** 41.0+
  - AES-256-GCM para credenciais
  - Key derivation com PBKDF2

**HTTP Client:**
- **httpx** 0.25+
  - Cliente HTTP async
  - Suporte a streaming
  - Timeout configurável

### 2.2 Frontend

**Framework:**
- **React** 18.2+ ou **Vue.js** 3.3+
  - Componentes reutilizáveis
- **TypeScript** 5.0+
  - Type safety

**HTTP Client:**
- **Axios** 1.6+
  - Interceptors para auth
  - Retry automático

**WebSocket:**
- **Socket.io-client** 4.6+
  - Atualização de progresso em tempo real

**UI Framework (Opcional):**
- **Tailwind CSS** 3.3+
- **Material-UI** ou **Ant Design**

### 2.3 Infraestrutura

**Containerização:**
- **Docker** 24.0+
- **Docker Compose** 2.23+

**Web Server:**
- **Nginx** 1.25+
  - Reverse proxy
  - SSL termination
  - Static files

**WSGI Server:**
- **Gunicorn** 21.2+
  - Workers: 4-8 (CPU cores * 2)
  - Worker class: uvicorn.workers.UvicornWorker

**Message Queue:**
- **Redis** 7.2+
  - Broker para Celery
  - Cache de sessões

---

## 3. Estrutura do Projeto

### 3.1 Estrutura de Diretórios

```
cloud-migrate/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app
│   │   ├── config.py              # Configurações
│   │   ├── database.py            # Conexão DB
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── auth.py        # Rotas de autenticação
│   │   │   │   ├── credentials.py # Rotas de credenciais
│   │   │   │   └── migrations.py  # Rotas de migrações
│   │   │   └── dependencies.py   # Dependencies (auth, etc)
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── credential.py
│   │   │   └── migration.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py            # Pydantic schemas
│   │   │   ├── credential.py
│   │   │   └── migration.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── credential_service.py
│   │   │   ├── migration_service.py
│   │   │   ├── encryption_service.py
│   │   │   ├── icloud_adapter.py
│   │   │   └── google_drive_adapter.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   ├── credential_repository.py
│   │   │   └── migration_repository.py
│   │   │
│   │   └── workers/
│   │       ├── __init__.py
│   │       ├── celery_app.py      # Celery app
│   │       └── tasks.py           # Background tasks
│   │
│   ├── alembic/                    # Migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── tsconfig.json
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 4. Modelos de Dados

### 4.1 Schema do Banco de Dados

#### Tabela: users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

#### Tabela: credentials

```sql
CREATE TABLE credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    service_type TEXT NOT NULL CHECK(service_type IN ('icloud', 'google_drive')),
    encrypted_credentials TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, service_type)
);

CREATE INDEX idx_credentials_user_id ON credentials(user_id);
CREATE INDEX idx_credentials_service_type ON credentials(service_type);
```

#### Tabela: migrations

```sql
CREATE TABLE migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending', 'in_progress', 'completed', 'failed', 'paused')),
    total_photos INTEGER DEFAULT 0,
    migrated_photos INTEGER DEFAULT 0,
    failed_photos INTEGER DEFAULT 0,
    started_at DATETIME,
    completed_at DATETIME,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_migrations_user_id ON migrations(user_id);
CREATE INDEX idx_migrations_status ON migrations(status);
CREATE INDEX idx_migrations_created_at ON migrations(created_at);
```

#### Tabela: migration_logs

```sql
CREATE TABLE migration_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    migration_id INTEGER NOT NULL,
    photo_name TEXT NOT NULL,
    photo_path TEXT,
    status TEXT NOT NULL CHECK(status IN ('pending', 'downloading', 'uploading', 'completed', 'failed')),
    error_message TEXT,
    file_size INTEGER,
    checksum TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (migration_id) REFERENCES migrations(id) ON DELETE CASCADE
);

CREATE INDEX idx_migration_logs_migration_id ON migration_logs(migration_id);
CREATE INDEX idx_migration_logs_status ON migration_logs(status);
```

---

## 5. APIs e Endpoints

### 5.1 Autenticação

#### POST /api/auth/register
Registra novo usuário.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2023-12-15T10:00:00Z"
}
```

#### GET /api/oauth/google/init
Inicia fluxo OAuth do Google Drive.

**Response:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?..."
}
```

#### GET /api/oauth/google/callback
Callback do OAuth do Google.

**Query Parameters:**
- `code`: Código de autorização
- `state`: Estado para validação

**Response:**
```json
{
  "success": true,
  "message": "Google Drive conectado com sucesso"
}
```

### 5.2 Credenciais

#### POST /api/credentials
Cria/atualiza credenciais do iCloud.

**Request:**
```json
{
  "service_type": "icloud",
  "apple_id": "user@icloud.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "id": 1,
  "service_type": "icloud",
  "created_at": "2023-12-15T10:00:00Z"
}
```

#### GET /api/credentials
Lista credenciais do usuário.

**Response:**
```json
{
  "credentials": [
    {
      "id": 1,
      "service_type": "icloud",
      "status": "configured",
      "created_at": "2023-12-15T10:00:00Z"
    },
    {
      "id": 2,
      "service_type": "google_drive",
      "status": "connected",
      "created_at": "2023-12-15T10:05:00Z"
    }
  ]
}
```

#### DELETE /api/credentials/{id}
Remove credenciais.

**Response:**
```json
{
  "success": true,
  "message": "Credenciais removidas com sucesso"
}
```

### 5.3 Migrações

#### POST /api/migrations
Inicia nova migração.

**Request:**
```json
{
  "options": {
    "preserve_structure": true,
    "skip_duplicates": true
  }
}
```

**Response:**
```json
{
  "id": 1,
  "status": "pending",
  "total_photos": 0,
  "migrated_photos": 0,
  "created_at": "2023-12-15T10:10:00Z"
}
```

#### GET /api/migrations
Lista migrações do usuário.

**Query Parameters:**
- `status`: Filtrar por status
- `page`: Número da página
- `limit`: Itens por página

**Response:**
```json
{
  "migrations": [
    {
      "id": 1,
      "status": "in_progress",
      "total_photos": 5234,
      "migrated_photos": 3402,
      "progress": 65.0,
      "started_at": "2023-12-15T10:10:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 20
}
```

#### GET /api/migrations/{id}
Detalhes de uma migração.

**Response:**
```json
{
  "id": 1,
  "status": "completed",
  "total_photos": 5234,
  "migrated_photos": 5200,
  "failed_photos": 34,
  "progress": 100.0,
  "started_at": "2023-12-15T10:10:00Z",
  "completed_at": "2023-12-15T10:52:00Z",
  "duration_minutes": 42
}
```

#### GET /api/migrations/{id}/progress
Progresso em tempo real (WebSocket ou polling).

**Response:**
```json
{
  "migration_id": 1,
  "status": "in_progress",
  "total_photos": 5234,
  "migrated_photos": 3402,
  "failed_photos": 0,
  "progress": 65.0,
  "current_photo": "IMG_2023_12_15.jpg",
  "speed_mbps": 2.5,
  "estimated_time_remaining_minutes": 18
}
```

#### POST /api/migrations/{id}/pause
Pausa migração.

**Response:**
```json
{
  "success": true,
  "status": "paused"
}
```

#### POST /api/migrations/{id}/resume
Retoma migração pausada.

**Response:**
```json
{
  "success": true,
  "status": "in_progress"
}
```

#### DELETE /api/migrations/{id}
Cancela migração.

**Response:**
```json
{
  "success": true,
  "message": "Migração cancelada"
}
```

---

## 6. Serviços e Lógica de Negócio

### 6.1 EncryptionService

Responsável por criptografar e descriptografar credenciais.

**Métodos:**
- `encrypt(plaintext: str, key: bytes) -> tuple[str, str]`: Retorna (encrypted, salt)
- `decrypt(encrypted: str, salt: str, key: bytes) -> str`: Retorna plaintext

**Implementação:**
- Algoritmo: AES-256-GCM
- Key derivation: PBKDF2-HMAC-SHA256
- Salt: 32 bytes aleatórios por credencial

### 6.2 iCloudAdapter

Adaptador para integração com iCloud API.

**Métodos:**
- `authenticate(apple_id: str, password: str) -> bool`
- `list_photos() -> list[Photo]`
- `download_photo(photo_id: str) -> bytes`
- `get_photo_metadata(photo_id: str) -> dict`

**Tratamento de Erros:**
- Rate limiting: Retry com backoff exponencial
- Timeout: 30 segundos por requisição
- 2FA: Retorna erro específico

### 6.3 GoogleDriveAdapter

Adaptador para integração com Google Drive API.

**Métodos:**
- `upload_file(file_data: bytes, filename: str, folder_id: str = None) -> str`
- `create_folder(name: str, parent_id: str = None) -> str`
- `get_storage_quota() -> dict`
- `refresh_token() -> bool`

**Tratamento de Erros:**
- Token expirado: Refresh automático
- Rate limiting: Retry com backoff
- Storage limit: Retorna erro específico

### 6.4 MigrationService

Orquestra o processo de migração.

**Fluxo:**
1. Valida credenciais (iCloud e Google Drive)
2. Lista fotos do iCloud
3. Cria registro de migração
4. Enfileira job de processamento
5. Atualiza progresso em tempo real
6. Notifica conclusão

**Recuperação de Falhas:**
- Retry automático para falhas temporárias
- Checkpointing: Salva progresso a cada 10 fotos
- Retomada: Pode retomar de último checkpoint

---

## 7. Background Jobs

### 7.1 Task: process_migration

Processa uma migração completa.

**Parâmetros:**
- `migration_id: int`
- `user_id: int`

**Fluxo:**
1. Busca credenciais do usuário
2. Conecta ao iCloud
3. Lista todas as fotos
4. Para cada foto:
   - Download do iCloud
   - Verifica checksum
   - Upload para Google Drive
   - Atualiza progresso
   - Salva log
5. Atualiza status final

**Retry:**
- Máximo 3 tentativas
- Backoff exponencial: 1s, 2s, 4s

### 7.2 Task: update_migration_progress

Atualiza progresso da migração (chamado periodicamente).

**Parâmetros:**
- `migration_id: int`

**Ação:**
- Calcula progresso baseado em migration_logs
- Atualiza campo `migrated_photos` na tabela migrations
- Publica evento via WebSocket (se disponível)

---

## 8. Segurança

### 8.1 Criptografia de Credenciais

**Algoritmo:** AES-256-GCM
**Key Management:** Chave mestra em variável de ambiente
**Salt:** Único por credencial (32 bytes)
**IV:** Gerado aleatoriamente para cada criptografia

**Implementação:**
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def encrypt_credentials(plaintext: str, master_key: bytes) -> tuple:
    salt = os.urandom(32)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(master_key)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return (ciphertext.hex(), salt.hex())
```

### 8.2 Validação de Entrada

- Todos os inputs validados com Pydantic
- Sanitização de strings
- Validação de tipos
- Limites de tamanho

### 8.3 Rate Limiting

- API: 100 requests/minuto por IP
- Migrações: 1 migração simultânea por usuário
- OAuth: 5 tentativas/hora por usuário

### 8.4 HTTPS

- Obrigatório em produção
- Certificados SSL válidos
- HSTS habilitado
- TLS 1.3 preferido

---

## 9. Performance

### 9.1 Otimizações

**Download/Upload:**
- Streaming para arquivos grandes (>10MB)
- Chunking: 8MB por chunk
- Paralelismo: 3 uploads simultâneos

**Banco de Dados:**
- Índices em campos frequentemente consultados
- WAL mode para melhor concorrência
- Connection pooling

**Cache:**
- Redis para metadados de fotos (TTL: 1 hora)
- Cache de tokens OAuth (TTL: 50 minutos)

### 9.2 Métricas Esperadas

- Tempo de resposta API: < 200ms (p95)
- Throughput de migração: 2-5 MB/s
- Uso de memória: < 500MB por worker
- CPU: < 50% durante migração normal

---

## 10. Monitoramento e Logging

### 10.1 Logging

**Níveis:**
- ERROR: Erros críticos
- WARNING: Avisos importantes
- INFO: Operações principais
- DEBUG: Detalhes de desenvolvimento

**Formato:**
```json
{
  "timestamp": "2023-12-15T10:00:00Z",
  "level": "INFO",
  "service": "migration",
  "migration_id": 1,
  "message": "Photo migrated successfully",
  "photo_name": "IMG_2023_12_15.jpg"
}
```

### 10.2 Métricas

**Coletar:**
- Taxa de sucesso de migrações
- Tempo médio de migração
- Taxa de erros por tipo
- Uso de recursos (CPU, memória, disco)

**Ferramentas:**
- Prometheus + Grafana (opcional)
- Logs estruturados em arquivo/ELK

---

## 11. Testes

### 11.1 Estrutura de Testes

**Unitários:**
- Services
- Repositories
- Utils
- Cobertura: > 80%

**Integração:**
- APIs
- Database
- External adapters (mocks)

**E2E:**
- Fluxo completo de migração
- Autenticação OAuth

### 11.2 Ferramentas

- **pytest** 7.4+
- **pytest-asyncio** 0.21+
- **pytest-cov** 4.1+
- **httpx** (para testes de API)
- **faker** (dados de teste)

---

## 12. Deployment

### 12.1 Variáveis de Ambiente

```bash
# Database
DATABASE_URL=sqlite:///./cloud_migrate.db

# Security
MASTER_ENCRYPTION_KEY=<32-byte-hex-key>
SECRET_KEY=<random-secret-key>
JWT_SECRET=<jwt-secret>

# OAuth
GOOGLE_CLIENT_ID=<google-client-id>
GOOGLE_CLIENT_SECRET=<google-client-secret>
GOOGLE_REDIRECT_URI=http://localhost:8000/api/oauth/google/callback

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# App
DEBUG=False
ENVIRONMENT=production
ALLOWED_ORIGINS=https://app.example.com
```

### 12.2 Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./data/db.sqlite
    volumes:
      - ./data:/app/data
    depends_on:
      - redis

  worker:
    build: ./backend
    command: celery -A app.workers.celery_app worker --loglevel=info
    depends_on:
      - redis
      - backend

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

---

**Documento gerado em:** [Data atual]  
**Versão:** 1.0  
**Status:** Pronto para implementação



