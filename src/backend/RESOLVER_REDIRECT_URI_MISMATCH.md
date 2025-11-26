# 🔧 Resolver Erro: redirect_uri_mismatch

## ❌ Erro
```
Erro 400: redirect_uri_mismatch
Não foi possível fazer login, porque esse app enviou uma solicitação inválida.
```

## 🔍 Causa
O **Redirect URI** configurado no **Google Cloud Console** não corresponde **exatamente** ao URI usado no código.

## ✅ Solução Rápida

### 1. Verificar o URI Configurado no Código

O URI usado no código é:
```
http://localhost:8000/api/v1/auth/oauth/google/callback
```

### 2. Configurar no Google Cloud Console

**Passo a passo:**

1. **Acesse o Google Cloud Console:**
   - URL: https://console.cloud.google.com/
   - Faça login com sua conta Google

2. **Selecione o Projeto:**
   - Escolha o projeto que contém suas credenciais OAuth

3. **Navegue até Credentials:**
   - Menu lateral: **APIs & Services** > **Credentials**
   - Ou acesse diretamente: https://console.cloud.google.com/apis/credentials

4. **Edite o OAuth 2.0 Client ID:**
   - Clique no **Client ID** que você está usando
   - Ou crie um novo: **+ CREATE CREDENTIALS** > **OAuth client ID**

5. **Adicione o Redirect URI:**
   - Role até a seção **Authorized redirect URIs**
   - Clique em **+ ADD URI**
   - Cole **EXATAMENTE** este URI:
     ```
     http://localhost:8000/api/v1/auth/oauth/google/callback
     ```
   - **⚠️ ATENÇÃO:** Deve ser **EXATAMENTE** igual, sem diferenças!

6. **Salve:**
   - Clique em **SAVE**
   - Aguarde alguns segundos para as alterações serem aplicadas

### 3. Verificar o Arquivo .env

Certifique-se de que o arquivo `.env` (não apenas `env.example`) está configurado:

```env
GOOGLE_CLIENT_ID=336894349454-eiuinuh8f8oblo6e55kceg5v5e8lanhk.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/google/callback
```

### 4. Reiniciar o Servidor

Após fazer as alterações:
```bash
# Pare o servidor (Ctrl+C)
# Reinicie o servidor
cd src/backend
python -m uvicorn app.main:app --reload
```

## 📋 Checklist de Verificação

- [ ] Redirect URI no Google Console: `http://localhost:8000/api/v1/auth/oauth/google/callback`
- [ ] Arquivo `.env` configurado (não apenas `env.example`)
- [ ] Backend rodando na porta 8000
- [ ] Servidor reiniciado após alterações
- [ ] Aguardou alguns segundos após salvar no Google Console

## ⚠️ Erros Comuns

### ❌ URI com diferenças sutis:
```
❌ http://localhost:8000/api/v1/auth/oauth/google/callback/  (barra no final)
❌ https://localhost:8000/api/v1/auth/oauth/google/callback  (https em vez de http)
❌ http://127.0.0.1:8000/api/v1/auth/oauth/google/callback  (127.0.0.1 em vez de localhost)
❌ http://localhost:8000/oauth/google/callback  (caminho incompleto)
```

### ✅ URI correto:
```
✅ http://localhost:8000/api/v1/auth/oauth/google/callback
```

## 🔍 Verificar Configuração Atual

Execute o script de verificação:

```bash
cd src/backend
python scripts/check_oauth_config.py
```

Este script mostrará:
- O Redirect URI configurado no código
- Instruções para configurar no Google Console

## 📸 Exemplo Visual

No Google Cloud Console, a seção deve ficar assim:

```
Authorized redirect URIs
┌─────────────────────────────────────────────────────────────┐
│ http://localhost:8000/api/v1/auth/oauth/google/callback    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Testar Após Configurar

1. Reinicie o servidor backend
2. Acesse o frontend
3. Clique em "Conectar Google Drive"
4. O erro não deve mais aparecer

## 💡 Dica

Se o erro persistir:
1. Aguarde 2-3 minutos (pode haver cache no Google)
2. Limpe o cache do navegador
3. Tente em modo anônimo/privado
4. Verifique os logs do backend para confirmar qual URI está sendo usado

## 📞 Ainda com Problemas?

Se após seguir todos os passos o erro persistir:
1. Verifique os logs do backend
2. Execute o script de verificação: `python scripts/check_oauth_config.py`
3. Confirme que o Client ID e Client Secret estão corretos
4. Verifique se o OAuth Consent Screen está configurado





