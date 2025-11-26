# Configuração do Google OAuth

## Problema Comum: "Solicitação Inválida"

Este erro geralmente ocorre quando o **Redirect URI** não está configurado corretamente no Google Cloud Console.

## Passo a Passo para Configurar

### 1. Acesse o Google Cloud Console

1. Vá para: https://console.cloud.google.com/
2. Selecione seu projeto (ou crie um novo)
3. Navegue até **APIs & Services** > **Credentials**

### 2. Configure o OAuth Consent Screen

1. Vá para **OAuth consent screen**
2. Escolha **External** (para desenvolvimento) ou **Internal** (para G Suite)
3. Preencha as informações obrigatórias:
   - App name: "Cloud Migrate"
   - User support email: seu email
   - Developer contact: seu email
4. Adicione os escopos necessários:
   - `https://www.googleapis.com/auth/drive.file`
5. Salve e continue

### 3. Configure as Credenciais OAuth 2.0

1. Vá para **Credentials** > **Create Credentials** > **OAuth client ID**
2. Selecione **Web application**
3. Configure:
   - **Name**: Cloud Migrate Web Client
   - **Authorized JavaScript origins**:
     ```
     http://localhost:8000
     http://localhost:3000
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:8000/api/v1/auth/oauth/google/callback
     ```
4. Clique em **Create**
5. Copie o **Client ID** e **Client Secret**

### 4. Configure no Backend

Atualize o arquivo `.env` (ou `env.example`) com as credenciais:

```env
GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/google/callback
```

### 5. Verificações Importantes

✅ **Redirect URI deve ser EXATAMENTE igual** no Google Console e no código:
- Google Console: `http://localhost:8000/api/v1/auth/oauth/google/callback`
- Código: `http://localhost:8000/api/v1/auth/oauth/google/callback`

✅ **URLs devem corresponder exatamente** (incluindo http/https, porta, caminho)

✅ **Escopos corretos**:
- `https://www.googleapis.com/auth/drive.file` (acesso a arquivos criados pela app)
- Ou `https://www.googleapis.com/auth/drive` (acesso completo ao Drive)

### 6. Para Produção

Quando for para produção, adicione também:
- **Authorized JavaScript origins**: `https://seu-dominio.com`
- **Authorized redirect URIs**: `https://seu-dominio.com/api/v1/auth/oauth/google/callback`

## Troubleshooting

### Erro: "redirect_uri_mismatch"
- Verifique se o redirect URI no Google Console está EXATAMENTE igual ao do código
- Certifique-se de que não há espaços extras ou diferenças de maiúsculas/minúsculas

### Erro: "invalid_client"
- Verifique se o Client ID e Client Secret estão corretos
- Certifique-se de que copiou os valores completos

### Erro: "access_denied"
- Verifique se o OAuth consent screen está configurado
- Verifique se os escopos estão corretos

### Erro: "invalid_grant"
- O código de autorização pode ter expirado (válido por 10 minutos)
- Tente novamente o fluxo completo

## Testando

1. Inicie o backend: `uvicorn app.main:app --reload`
2. Acesse: `http://localhost:8000/api/v1/auth/oauth/google/init`
3. Você receberá uma `auth_url`
4. Abra essa URL no navegador
5. Faça login e autorize
6. Você será redirecionado para o callback

## Nota de Segurança

⚠️ **NUNCA** commite o arquivo `.env` com credenciais reais no Git!
- Use `.env.example` para templates
- Adicione `.env` ao `.gitignore`
- Use variáveis de ambiente em produção



