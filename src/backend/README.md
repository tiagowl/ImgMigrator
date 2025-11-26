# Cloud Migrate Backend API

Backend API for migrating photos from iCloud to Google Drive.

## Features

- RESTful API with FastAPI
- OAuth 2.0 authentication with Google Drive
- Secure credential storage with AES-256-GCM encryption
- Background job processing with Celery
- SQLite database (can be migrated to PostgreSQL)

## Setup

### Local Development

1. Install dependencies:

**Instalação padrão:**
```powershell
# Atualizar pip primeiro
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

**Se houver problemas com compilação (Rust):**
```powershell
# Use o arquivo requirements-simple.txt que tem versões com wheels disponíveis
pip install -r requirements-simple.txt
```

**Nota:** O `requirements.txt` foi atualizado com versões que têm wheels pré-compilados disponíveis para Python 3.13, então não deve ser necessário compilar.

2. Copy environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Initialize database:
```bash
python -c "from app.database import init_db; init_db()"
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

5. Run Celery worker (in another terminal):
```bash
celery -A app.workers.celery_app worker --loglevel=info
```

### Render Deployment (Recomendado)

O Render é a plataforma recomendada para este projeto, pois suporta:
- ✅ Workers Celery
- ✅ PostgreSQL
- ✅ Redis
- ✅ Processos de longa duração

**Guia completo**: Veja [RENDER_DEPLOY.md](./RENDER_DEPLOY.md)

**Resumo rápido**:
1. Crie conta no Render: https://render.com
2. Crie PostgreSQL e Redis no dashboard
3. Crie Web Service apontando para `src/backend`
4. Crie Background Worker para Celery
5. Configure variáveis de ambiente
6. Inicialize o banco de dados

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `MASTER_ENCRYPTION_KEY`
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `GOOGLE_REDIRECT_URI`
   - `REDIS_URL`
   - `CELERY_BROKER_URL`
   - `CELERY_RESULT_BACKEND`

⚠️ **Nota**: Vercel não suporta workers Celery. Para produção, use Render.

## API Documentation

Once running, access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `GET /api/v1/auth/oauth/google/init` - Initialize Google OAuth
- `GET /api/v1/auth/oauth/google/callback` - OAuth callback

### Credentials
- `POST /api/v1/credentials` - Create/update credentials
- `GET /api/v1/credentials` - List user credentials
- `DELETE /api/v1/credentials/{id}` - Delete credential

### Migrations
- `POST /api/v1/migrations` - Create new migration
- `GET /api/v1/migrations` - List migrations
- `GET /api/v1/migrations/{id}` - Get migration details
- `GET /api/v1/migrations/{id}/progress` - Get migration progress
- `POST /api/v1/migrations/{id}/pause` - Pause migration
- `POST /api/v1/migrations/{id}/resume` - Resume migration
- `DELETE /api/v1/migrations/{id}` - Cancel migration

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI app
├── config.py            # Configuration
├── database.py          # Database setup
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── repositories/        # Data access layer
├── services/            # Business logic
├── api/                 # API routes
│   └── routes/
└── workers/            # Celery tasks
```

## OAuth Configuration

### Verificar Configuração

Execute o script de verificação:

```bash
python scripts/verify_oauth.py
```

### Configurar Google OAuth

1. Acesse: https://console.cloud.google.com/apis/credentials
2. Crie um OAuth 2.0 Client ID (tipo: Web application)
3. Configure o **Authorized redirect URI**:
   ```
   http://localhost:8000/api/v1/auth/oauth/google/callback
   ```
4. Configure **Authorized JavaScript origins**:
   ```
   http://localhost:8000
   http://localhost:3000
   ```

⚠️ **IMPORTANTE**: O redirect URI deve ser EXATAMENTE igual no Google Console e no código!

Para mais detalhes, veja: [OAUTH_SETUP.md](./OAUTH_SETUP.md)

## Notes

- **Render (Recomendado)**: Suporta PostgreSQL, Redis e workers Celery nativamente.
- **Vercel**: SQLite files are ephemeral. Celery workers need to run separately (not on Vercel serverless).
- For production, use PostgreSQL and Redis hosted services.
- OAuth redirect URI must match exactly between Google Console and code configuration.
- Para deploy no Render, veja o guia completo em [RENDER_DEPLOY.md](./RENDER_DEPLOY.md).

