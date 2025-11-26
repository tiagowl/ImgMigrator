# Guia de Migrações do Banco de Dados

## Problema Resolvido: Colunas nonce e expires_at

O erro `no such column: credentials.nonce` ocorreu porque o modelo `Credential` foi atualizado para incluir as colunas `nonce` e `expires_at`, mas o banco de dados não foi migrado.

### ✅ Solução Aplicada

As colunas foram adicionadas com sucesso:
- ✅ `nonce` - Para armazenar o nonce do AES-GCM (tokens OAuth)
- ✅ `expires_at` - Para armazenar a data de expiração dos tokens OAuth

## Scripts de Migração

### 1. Adicionar colunas nonce e expires_at

```bash
cd src/backend
python scripts/migrate_add_nonce_column.py
```

Este script:
- Verifica se as colunas já existem
- Adiciona `nonce` se não existir
- Adiciona `expires_at` se não existir
- É idempotente (pode ser executado múltiplas vezes)

## Como Funciona

O SQLAlchemy usa `Base.metadata.create_all()` que:
- ✅ Cria tabelas se não existirem
- ❌ **NÃO** adiciona colunas a tabelas existentes

Por isso, precisamos de scripts de migração manuais para SQLite.

## Estrutura Atual da Tabela credentials

```sql
CREATE TABLE credentials (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    service_type VARCHAR NOT NULL,
    encrypted_credentials VARCHAR NOT NULL,
    salt VARCHAR NOT NULL,
    nonce VARCHAR,                    -- ✅ Adicionada
    expires_at DATETIME,              -- ✅ Adicionada
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Próximas Migrações

Se precisar adicionar mais colunas no futuro:

1. **Atualize o modelo** (`app/models/credential.py`)
2. **Crie um script de migração** (exemplo em `scripts/migrate_add_nonce_column.py`)
3. **Execute o script** antes de usar o novo código

## Verificar Estrutura do Banco

Para verificar a estrutura atual:

```bash
cd src/backend
python -c "
from sqlalchemy import text
from app.database import SessionLocal
db = SessionLocal()
result = db.execute(text('PRAGMA table_info(credentials)'))
for row in result:
    print(f'{row[1]} ({row[2]})')
db.close()
"
```

## Notas Importantes

- ⚠️ **Backup**: Sempre faça backup do banco antes de migrações em produção
- ✅ **Idempotência**: Scripts de migração devem ser idempotentes
- 🔍 **Verificação**: Sempre verifique se as colunas já existem antes de adicionar
- 📝 **Logs**: Scripts devem mostrar claramente o que está sendo feito

## Alternativa: Recriar Banco (Desenvolvimento)

Se estiver em desenvolvimento e não se importar em perder dados:

```bash
# Deletar banco
rm cloud_migrate.db

# Recriar banco
python -c "from app.database import init_db; init_db()"
```

Isso recriará todas as tabelas com a estrutura atual dos modelos.





