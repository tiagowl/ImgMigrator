#!/usr/bin/env python3
"""Script para verificar configuração OAuth do Google."""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings

def check_oauth_config():
    """Verifica a configuração OAuth."""
    print("=" * 60)
    print("Verificação de Configuração OAuth do Google")
    print("=" * 60)
    print()
    
    # Verificar Client ID
    if settings.GOOGLE_CLIENT_ID:
        print(f"✅ GOOGLE_CLIENT_ID: {settings.GOOGLE_CLIENT_ID}")
    else:
        print("❌ GOOGLE_CLIENT_ID: NÃO CONFIGURADO")
    
    # Verificar Client Secret
    if settings.GOOGLE_CLIENT_SECRET:
        print(f"✅ GOOGLE_CLIENT_SECRET: {'*' * 20} (configurado)")
    else:
        print("❌ GOOGLE_CLIENT_SECRET: NÃO CONFIGURADO")
    
    # Verificar Redirect URI
    print()
    print(f"📍 GOOGLE_REDIRECT_URI: {settings.GOOGLE_REDIRECT_URI}")
    print()
    print("=" * 60)
    print("INSTRUÇÕES PARA GOOGLE CLOUD CONSOLE:")
    print("=" * 60)
    print()
    print("1. Acesse: https://console.cloud.google.com/")
    print("2. Vá para: APIs & Services > Credentials")
    print("3. Edite seu OAuth 2.0 Client ID")
    print("4. Em 'Authorized redirect URIs', adicione EXATAMENTE:")
    print()
    print(f"   {settings.GOOGLE_REDIRECT_URI}")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - O URI deve ser EXATAMENTE igual ao mostrado acima")
    print("   - Inclua http:// (não https:// para localhost)")
    print("   - Inclua a porta :8000")
    print("   - Inclua o caminho completo")
    print("   - Não adicione barra no final")
    print("   - Case-sensitive (minúsculas)")
    print()
    print("=" * 60)
    
    # Verificar se está tudo configurado
    if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET and settings.GOOGLE_REDIRECT_URI:
        print("✅ Configuração básica OK")
        print("⚠️  Verifique se o Redirect URI está configurado no Google Console")
    else:
        print("❌ Configuração incompleta")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(check_oauth_config())


