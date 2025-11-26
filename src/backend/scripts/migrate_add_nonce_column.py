#!/usr/bin/env python3
"""Script para adicionar colunas nonce e expires_at à tabela credentials."""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine, SessionLocal
from app.config import settings


def migrate_credentials_table():
    """Adiciona colunas nonce e expires_at à tabela credentials."""
    print("=" * 60)
    print("Migração: Adicionando colunas nonce e expires_at")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    
    try:
        # Verificar se as colunas já existem
        print("Verificando estrutura atual da tabela...")
        result = db.execute(text("PRAGMA table_info(credentials)"))
        columns = [row[1] for row in result.fetchall()]
        
        print(f"Colunas existentes: {', '.join(columns)}")
        print()
        
        # Adicionar coluna nonce se não existir
        if 'nonce' not in columns:
            print("Adicionando coluna 'nonce'...")
            db.execute(text("ALTER TABLE credentials ADD COLUMN nonce VARCHAR"))
            db.commit()
            print("✅ Coluna 'nonce' adicionada com sucesso")
        else:
            print("✅ Coluna 'nonce' já existe")
        
        # Adicionar coluna expires_at se não existir
        if 'expires_at' not in columns:
            print("Adicionando coluna 'expires_at'...")
            db.execute(text("ALTER TABLE credentials ADD COLUMN expires_at DATETIME"))
            db.commit()
            print("✅ Coluna 'expires_at' adicionada com sucesso")
        else:
            print("✅ Coluna 'expires_at' já existe")
        
        print()
        print("=" * 60)
        print("✅ Migração concluída com sucesso!")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        db.rollback()
        print()
        print("=" * 60)
        print(f"❌ Erro durante a migração: {str(e)}")
        print("=" * 60)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    print(f"Banco de dados: {settings.DATABASE_URL}")
    print()
    exit(migrate_credentials_table())





