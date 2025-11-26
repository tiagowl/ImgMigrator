# Guia de Deploy no Render

Este guia explica como fazer o deploy do backend Cloud Migrate no Render.

## 📋 Pré-requisitos

1. Conta no Render: https://render.com
2. Repositório Git (GitHub, GitLab ou Bitbucket)
3. Credenciais do Google OAuth configuradas

## 🚀 Passo a Passo

### 1. Preparar o Repositório

Os seguintes arquivos já estão configurados:
- ✅ `Procfile` - Define processos web e worker
- ✅ `runtime.txt` - Especifica versão do Python
- ✅ `render.yaml` - Configuração automatizada (opcional)
- ✅ `requirements.txt` - Inclui `psycopg2-binary` para PostgreSQL

### 2. Criar Banco de Dados PostgreSQL

1. Acesse: https://dashboard.render.com
2. Clique em **New +** → **PostgreSQL**
3. Configure:
   - **Name**: `cloud-migrate-db`
   - **Database**: `cloud_migrate`
   - **User**: `cloud_migrate_user`
   - **Region**: Escolha a mais próxima dos seus usuários
   - **Plan**: Free (ou Starter para produção)
4. Clique em **Create Database**
5. **Anote as URLs**:
   - **Internal Database URL**: Para uso dentro do Render
   - **External Database URL**: Para acesso externo (se necessário)

### 3. Criar Redis

1. Clique em **New +** → **Redis**
2. Configure:
   - **Name**: `cloud-migrate-redis`
   - **Region**: Mesma do PostgreSQL
   - **Plan**: Free (25MB) ou Starter para produção
3. Clique em **Create Redis**
4. **Anote as URLs**:
   - **Internal Redis URL**: Para uso dentro do Render
   - **External Redis URL**: Para acesso externo (se necessário)

### 4. Criar Web Service (API)

1. Clique em **New +** → **Web Service**
2. Conecte seu repositório Git
3. Configure:
   - **Name**: `cloud-migrate-api`
   - **Region**: Mesma dos outros serviços
   - **Branch**: `main` (ou `master`)
   - **Root Directory**: `src/backend` ⚠️ **IMPORTANTE**
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (ou Starter para produção)

4. **Environment Variables**:
   ```
   DEBUG=False
   ENVIRONMENT=production
   DATABASE_URL=<Internal Database URL do PostgreSQL>
   SECRET_KEY=<gere uma chave aleatória segura>
   MASTER_ENCRYPTION_KEY=<gere uma chave hex de 64 caracteres>
   GOOGLE_CLIENT_ID=<seu-client-id>
   GOOGLE_CLIENT_SECRET=<seu-client-secret>
   GOOGLE_REDIRECT_URI=https://cloud-migrate-api.onrender.com/api/v1/auth/oauth/google/callback
   REDIS_URL=<Internal Redis URL>
   CELERY_BROKER_URL=<Internal Redis URL>
   CELERY_RESULT_BACKEND=<Internal Redis URL>
   ALLOWED_ORIGINS=https://seu-frontend.onrender.com,http://localhost:3000
   PORT=10000
   ```

   ⚠️ **IMPORTANTE**:
   - Use **Internal URLs** para serviços no mesmo ambiente
   - `GOOGLE_REDIRECT_URI` deve usar a URL real do Render (será algo como `https://cloud-migrate-api.onrender.com`)
   - `ALLOWED_ORIGINS` deve incluir a URL do frontend

5. Clique em **Create Web Service**

### 5. Criar Background Worker (Celery)

1. Clique em **New +** → **Background Worker**
2. Conecte o mesmo repositório
3. Configure:
   - **Name**: `cloud-migrate-worker`
   - **Region**: Mesma do Web Service
   - **Branch**: `main`
   - **Root Directory**: `src/backend` ⚠️ **IMPORTANTE**
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A app.workers.celery_app worker --loglevel=info`
   - **Plan**: Free (ou Starter)

4. **Environment Variables**:
   - Copie **todas** as variáveis do Web Service
   - Certifique-se de usar as mesmas URLs internas

5. Clique em **Create Background Worker**

### 6. Atualizar Google OAuth Console

1. Acesse: https://console.cloud.google.com/apis/credentials
2. Edite seu **OAuth 2.0 Client ID**
3. Adicione **Authorized redirect URIs**:
   ```
   https://cloud-migrate-api.onrender.com/api/v1/auth/oauth/google/callback
   ```
   ⚠️ Substitua `cloud-migrate-api` pelo nome real do seu serviço

4. Adicione **Authorized JavaScript origins**:
   ```
   https://cloud-migrate-api.onrender.com
   https://seu-frontend.onrender.com
   ```

### 7. Inicializar Banco de Dados

Após o deploy, inicialize o banco de dados:

**Opção 1: Via Render Shell**
1. No Web Service, vá em **Shell**
2. Execute:
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

**Opção 2: Criar Endpoint Temporário**
Adicione em `app/api/routes/admin.py`:
```python
from fastapi import APIRouter
from app.database import init_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/init-db")
async def initialize_database():
    """Initialize database (temporary endpoint)."""
    init_db()
    return {"message": "Database initialized successfully"}
```

Depois, acesse: `https://seu-api.onrender.com/admin/init-db`

⚠️ **Remova este endpoint após inicializar!**

### 8. Verificar Deploy

1. Acesse: `https://seu-api.onrender.com/docs`
2. Teste o endpoint `/health`
3. Verifique os logs:
   - **Web Service** → **Logs**
   - **Background Worker** → **Logs**

## 🔧 Configurações Importantes

### Root Directory

Se seu repositório tem a estrutura:
```
projeto/
├── src/
│   └── backend/
│       ├── app/
│       ├── requirements.txt
│       └── ...
└── ...
```

Configure **Root Directory** como: `src/backend`

Se o backend está na raiz do repositório, deixe vazio.

### Variáveis de Ambiente

- **Internal URLs**: Use para comunicação entre serviços no Render
- **External URLs**: Use apenas para acesso externo
- **GOOGLE_REDIRECT_URI**: Deve ser a URL real do Render (HTTPS)
- **ALLOWED_ORIGINS**: Deve incluir a URL exata do frontend (sem barra final)

### Health Check

O Render verifica automaticamente o endpoint `/health`. Certifique-se de que está funcionando.

## 🐛 Troubleshooting

### Erro de Importação

- Verifique o **Root Directory**
- Confirme que `requirements.txt` está no lugar certo
- Verifique os logs de build

### Worker Não Inicia

- Verifique as variáveis de ambiente do worker
- Confirme que Redis está acessível
- Veja os logs do worker

### Timeout

- Free tier tem limite de 15 minutos de inatividade
- Considere upgrade ou use serviço de keep-alive

### Banco de Dados Não Conecta

- Use **Internal Database URL** (não External)
- Verifique se o banco está no mesmo ambiente
- Confirme que `psycopg2-binary` está no `requirements.txt`

### CORS

- Verifique `ALLOWED_ORIGINS` com a URL exata do frontend
- Inclua `https://` e sem barra no final
- Exemplo: `https://meu-frontend.onrender.com` (não `https://meu-frontend.onrender.com/`)

## 💰 Custos

### Free Tier
- ✅ Web Service: Gratuito (pode hibernar após 15 min)
- ✅ PostgreSQL: Gratuito (90 dias, depois $7/mês)
- ✅ Redis: Gratuito (25MB)
- ✅ Background Worker: Gratuito

### Starter Tier (Recomendado para Produção)
- 💰 Web Service: $7/mês (sem hibernação)
- 💰 PostgreSQL: $7/mês
- 💰 Redis: $10/mês
- 💰 Background Worker: $7/mês

## 📝 Estrutura de Arquivos

```
src/backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   └── ...
├── requirements.txt
├── Procfile          ✅ Criado
├── render.yaml       ✅ Criado (opcional)
├── runtime.txt       ✅ Criado
└── .env.example
```

## 🚀 Próximos Passos

1. ✅ Configurar domínio customizado (opcional)
2. ✅ Configurar SSL (automático no Render)
3. ✅ Configurar monitoramento
4. ✅ Configurar backups do banco de dados
5. ✅ Remover endpoint de inicialização após setup

## 📚 Recursos

- [Documentação Render](https://render.com/docs)
- [Render Python Guide](https://render.com/docs/python)
- [Render PostgreSQL](https://render.com/docs/databases)
- [Render Redis](https://render.com/docs/redis)

---

**Última atualização**: 2024
**Versão**: 1.0




