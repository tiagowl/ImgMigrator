# Correção do Fluxo OAuth do Google

## Problema Identificado

O erro ao autenticar com o Google durante o fluxo OAuth pode ter várias causas:

### 1. **Redirect URI Incorreto** (PRINCIPAL)
O `GOOGLE_REDIRECT_URI` estava configurado como:
```
http://localhost:3000/api/v1/auth/oauth/google/callback
```

Mas o endpoint de callback está no **backend** (porta 8000), não no frontend (porta 3000).

**Correção aplicada:**
```
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/google/callback
```

### 2. **Falta de Tratamento de Erros do Google**
O callback não estava tratando erros retornados diretamente pelo Google (parâmetros `error` e `error_description`).

**Correção aplicada:**
- Adicionado tratamento para parâmetros `error` e `error_description` na URL de callback
- Melhorado tratamento de exceções com logging detalhado
- Mensagens de erro mais informativas

### 3. **Validação de Código Ausente**
O callback não verificava se o código de autorização estava presente antes de tentar trocá-lo por tokens.

**Correção aplicada:**
- Validação do parâmetro `code` antes de processar
- Mensagens de erro claras quando o código está ausente

## Mudanças Implementadas

### Backend (`src/backend/app/api/routes/auth.py`)

1. **Tratamento de erros do Google:**
   ```python
   if error:
       error_msg = error_description or error
       # Redireciona com mensagem de erro
   ```

2. **Validação de código:**
   ```python
   if not code:
       # Redireciona com erro informativo
   ```

3. **Logging detalhado:**
   - Logs em cada etapa do processo
   - Facilita debugging de problemas

4. **Melhor tratamento de exceções:**
   - Captura diferentes tipos de exceções
   - Mensagens de erro mais específicas

### Backend (`src/backend/app/services/auth_service.py`)

1. **Validação de redirect URI:**
   ```python
   if not settings.GOOGLE_REDIRECT_URI:
       raise ValueError("GOOGLE_REDIRECT_URI não configurado")
   ```

2. **Melhor extração de erros:**
   - Tenta extrair detalhes de erros da resposta HTTP
   - Mensagens mais informativas

### Configuração (`src/backend/env.example`)

1. **Redirect URI corrigido:**
   ```
   GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/google/callback
   ```

## Verificações Necessárias

### 1. Google Cloud Console

Certifique-se de que o **Redirect URI** está configurado corretamente no Google Cloud Console:

1. Acesse: https://console.cloud.google.com/
2. Vá para **APIs & Services** > **Credentials**
3. Edite seu **OAuth 2.0 Client ID**
4. Em **Authorized redirect URIs**, adicione:
   ```
   http://localhost:8000/api/v1/auth/oauth/google/callback
   ```
5. **IMPORTANTE:** O URI deve ser **exatamente igual** ao configurado no `.env`

### 2. Arquivo `.env` do Backend

Certifique-se de que o arquivo `.env` (não apenas `env.example`) está configurado:

```env
GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/google/callback
```

### 3. Verificar Logs

Se ainda houver problemas, verifique os logs do backend. Agora há logging detalhado em cada etapa:
- Troca de código por token
- Obtenção de informações do usuário
- Salvamento de credenciais
- Erros específicos

## Fluxo Corrigido

1. Usuário clica em "Conectar Google Drive"
2. Frontend redireciona para URL de autorização do Google
3. Usuário autoriza no Google
4. **Google redireciona para:** `http://localhost:8000/api/v1/auth/oauth/google/callback?code=...`
5. Backend:
   - Valida código
   - Troca código por tokens
   - Obtém informações do usuário
   - Salva credenciais criptografadas
   - Redireciona para frontend com status
6. Frontend mostra notificação de sucesso/erro

## Erros Comuns e Soluções

### "redirect_uri_mismatch"
**Causa:** O redirect URI no Google Console não corresponde ao configurado no código.

**Solução:** Verifique que ambos são **exatamente iguais**:
- Google Console: `http://localhost:8000/api/v1/auth/oauth/google/callback`
- Código: `http://localhost:8000/api/v1/auth/oauth/google/callback`

### "invalid_grant"
**Causa:** Código de autorização já foi usado ou expirou.

**Solução:** Tente autenticar novamente. Códigos de autorização são de uso único.

### "access_denied"
**Causa:** Usuário negou a autorização.

**Solução:** Usuário precisa autorizar novamente.

## Próximos Passos

1. **Atualize o `.env`** com o redirect URI correto
2. **Verifique o Google Cloud Console** e adicione o redirect URI
3. **Teste o fluxo** novamente
4. **Verifique os logs** se ainda houver problemas





