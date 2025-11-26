# Otimização do OAuth do Google Drive

## Resumo das Melhorias

Este documento descreve as otimizações implementadas no processo de OAuth do Google para permitir a migração de fotos do iCloud para o Google Drive.

## Mudanças Implementadas

### 1. Modelo de Credenciais (`app/models/credential.py`)
- ✅ Adicionado campo `nonce` para suporte a AES-GCM
- ✅ Adicionado campo `expires_at` para rastrear expiração de tokens OAuth

### 2. Serviço de Criptografia (`app/services/encryption_service.py`)
- ✅ Atualizado para retornar `(ciphertext, salt, nonce)` separadamente
- ✅ Adicionado `encrypt_oauth_tokens()` para criptografar tokens OAuth
- ✅ Adicionado `decrypt_oauth_tokens()` para descriptografar tokens OAuth

### 3. Serviço de Autenticação (`app/services/auth_service.py`)
- ✅ Atualizado escopo OAuth para `https://www.googleapis.com/auth/drive` (acesso completo)
- ✅ Adicionado `access_type="offline"` e `prompt="consent"` para garantir refresh token
- ✅ Adicionado `refresh_google_token()` para renovar tokens expirados
- ✅ Adicionado `get_user_info()` para obter informações do usuário Google

### 4. Serviço de Credenciais (`app/services/credential_service.py`)
- ✅ Adicionado `create_google_oauth_credential()` para salvar tokens OAuth criptografados
- ✅ Adicionado `get_google_oauth_tokens()` para recuperar tokens descriptografados
- ✅ Adicionado `is_google_token_expired()` para verificar expiração
- ✅ Atualizado `create_credential()` para suportar nonce

### 5. Serviço do Google Drive (`app/services/google_drive_service.py`) - NOVO
- ✅ Criado serviço completo para operações no Google Drive
- ✅ Gerenciamento automático de tokens (refresh quando necessário)
- ✅ `upload_file()` - Upload de arquivos para o Drive
- ✅ `create_folder()` - Criação de pastas
- ✅ `get_storage_quota()` - Verificação de quota de armazenamento
- ✅ `verify_connection()` - Verificação de conexão

### 6. Rotas de Autenticação (`app/api/routes/auth.py`)
- ✅ Melhorado `/oauth/google/init` para incluir `user_id` na resposta
- ✅ Melhorado `/oauth/google/callback` para:
  - Trocar código por tokens
  - Obter informações do usuário Google
  - Criar/atualizar usuário se necessário
  - Salvar tokens criptografados
  - Retornar página HTML que fecha popup e notifica parent window

### 7. Rotas de Credenciais (`app/api/routes/credentials.py`)
- ✅ Melhorado `/credentials` para mostrar status de conexão (connected/expired/error)
- ✅ Adicionado `/credentials/google/verify` para verificar conexão e obter quota

## Fluxo OAuth Otimizado

### 1. Inicialização
```
GET /api/v1/auth/oauth/google/init?user_id=1
→ Retorna: { auth_url, state, user_id, redirect_uri }
```

### 2. Autorização do Usuário
- Frontend abre popup com `auth_url`
- Usuário autoriza no Google
- Google redireciona para `/api/v1/auth/oauth/google/callback?code=...`

### 3. Callback e Armazenamento
- Backend troca código por tokens (access_token + refresh_token)
- Obtém informações do usuário Google
- Cria/atualiza usuário no banco
- **Salva tokens criptografados** no banco de dados
- Retorna página HTML que fecha popup e notifica frontend

### 4. Uso nas Migrações
- `GoogleDriveService` recupera tokens do banco
- Verifica expiração automaticamente
- Renova tokens quando necessário
- Usa tokens para upload de fotos

## Segurança

- ✅ Tokens OAuth são **criptografados** usando AES-256-GCM
- ✅ Cada token tem seu próprio salt e nonce
- ✅ Refresh tokens são armazenados para renovação automática
- ✅ Tokens expirados são detectados e renovados automaticamente

## Próximos Passos

1. **Integrar com Migração**: Atualizar `process_migration_task` para usar `GoogleDriveService`
2. **Frontend**: Atualizar frontend para:
   - Abrir popup OAuth
   - Escutar mensagens do callback
   - Atualizar UI quando conexão for estabelecida
3. **Testes**: Testar fluxo completo de OAuth e upload de arquivos

## Endpoints Disponíveis

### Autenticação
- `GET /api/v1/auth/oauth/google/init?user_id=1` - Iniciar OAuth
- `GET /api/v1/auth/oauth/google/callback?code=...` - Callback OAuth

### Credenciais
- `GET /api/v1/credentials` - Listar credenciais com status
- `GET /api/v1/credentials/google/verify` - Verificar conexão Google Drive
- `DELETE /api/v1/credentials/{id}` - Remover credenciais

## Exemplo de Uso

```python
from app.services.google_drive_service import GoogleDriveService
from app.database import SessionLocal

db = SessionLocal()
user_id = 1

# Criar serviço
drive_service = GoogleDriveService(db, user_id)

# Verificar conexão
is_connected = await drive_service.verify_connection()

# Upload de arquivo
file_data = b"..."
result = await drive_service.upload_file(
    file_data=file_data,
    filename="photo.jpg",
    mime_type="image/jpeg"
)

print(f"Arquivo enviado: {result['id']}")
```

## Notas Importantes

1. **Escopo OAuth**: O escopo foi alterado para `https://www.googleapis.com/auth/drive` para permitir upload de arquivos
2. **Refresh Token**: O sistema solicita `access_type="offline"` e `prompt="consent"` para garantir refresh token
3. **Expiração**: Tokens são renovados automaticamente quando expirados
4. **Criptografia**: Todos os tokens são criptografados antes de serem salvos no banco



