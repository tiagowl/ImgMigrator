# Configuração do Google OAuth - Resolver redirect_uri_mismatch

## Erro: redirect_uri_mismatch

Este erro ocorre quando o **Redirect URI** configurado no Google Cloud Console **não corresponde exatamente** ao URI usado no código.

## Solução Passo a Passo

### 1. Verificar o Redirect URI no Código

O redirect URI usado no código está em:
- `src/backend/app/config.py` → `GOOGLE_REDIRECT_URI`
- `src/backend/env.example` → `GOOGLE_REDIRECT_URI`

**URI Padrão:**
```
http://localhost:8000/api/v1/auth/oauth/google/callback
```

### 2. Configurar no Google Cloud Console

1. **Acesse o Google Cloud Console:**
   - https://console.cloud.google.com/

2. **Navegue até Credentials:**
   - Selecione seu projeto
   - Vá para **APIs & Services** > **Credentials**

3. **Edite seu OAuth 2.0 Client ID:**
   - Clique no Client ID que você está usando
   - Ou crie um novo: **Create Credentials** > **OAuth client ID**

4. **Configure o Redirect URI:**
   - Em **Authorized redirect URIs**, adicione:
   ```
   http://localhost:8000/api/v1/auth/oauth/google/callback
   ```
   
   **⚠️ IMPORTANTE:**
   - O URI deve ser **EXATAMENTE igual** ao do código
   - Inclua `http://` (não `https://` para localhost)
   - Inclua a porta `:8000`
   - Inclua o caminho completo `/api/v1/auth/oauth/google/callback`
   - Não adicione barra no final
   - Case-sensitive (minúsculas)

5. **Salve as alterações**

### 3. Verificar o Arquivo .env

Certifique-se de que o arquivo `.env` (não apenas `env.example`) está configurado:

```env
GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/google/callback
```

### 4. Verificações Adicionais

#### Para Desenvolvimento Local:
- ✅ URI: `http://localhost:8000/api/v1/auth/oauth/google/callback`
- ✅ Backend rodando na porta 8000
- ✅ `.env` configurado corretamente

#### Para Produção:
Se você estiver usando em produção, adicione também o URI de produção:
```
https://seu-dominio.com/api/v1/auth/oauth/google/callback
```

### 5. Reiniciar o Servidor

Após fazer as alterações:
1. Pare o servidor backend
2. Reinicie o servidor backend
3. Tente autenticar novamente

## Checklist de Verificação

- [ ] Redirect URI no Google Console é **exatamente igual** ao do código
- [ ] Arquivo `.env` está configurado (não apenas `env.example`)
- [ ] Backend está rodando na porta 8000
- [ ] Servidor foi reiniciado após alterações
- [ ] Não há espaços extras ou caracteres especiais no URI
- [ ] URI usa `http://` para localhost (não `https://`)

## Exemplo de Configuração Correta

### Google Cloud Console:
```
Authorized redirect URIs:
http://localhost:8000/api/v1/auth/oauth/google/callback
```

### Arquivo .env:
```env
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/oauth/google/callback
```

### Código (app/config.py):
```python
GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/oauth/google/callback"
```

Todos os três devem ser **idênticos**!

## Troubleshooting

### Erro persiste após configurar?
1. Verifique se salvou as alterações no Google Console
2. Aguarde alguns minutos (pode haver cache)
3. Limpe o cache do navegador
4. Tente em modo anônimo/privado
5. Verifique os logs do backend para ver qual URI está sendo usado

### Múltiplos Ambientes?
Se você tem desenvolvimento e produção, adicione ambos os URIs no Google Console:
```
http://localhost:8000/api/v1/auth/oauth/google/callback
https://seu-dominio.com/api/v1/auth/oauth/google/callback
```

## Comandos Úteis

### Verificar configuração atual:
```bash
cd src/backend
python -c "from app.config import settings; print(f'Redirect URI: {settings.GOOGLE_REDIRECT_URI}')"
```

### Verificar se o servidor está rodando na porta correta:
```bash
# Verificar porta 8000
netstat -an | grep 8000
# ou
lsof -i :8000
```


