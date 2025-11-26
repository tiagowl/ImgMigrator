#!/usr/bin/env python3
"""Script para verificar configuração do OAuth."""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings

def verify_oauth_config():
    """Verifica se a configuração OAuth está correta."""
    print("🔍 Verificando configuração OAuth...\n")
    
    errors = []
    warnings = []
    
    # Verificar Client ID
    if not settings.GOOGLE_CLIENT_ID:
        errors.append("❌ GOOGLE_CLIENT_ID não está configurado")
    elif not settings.GOOGLE_CLIENT_ID.endswith('.apps.googleusercontent.com'):
        warnings.append("⚠️  GOOGLE_CLIENT_ID pode estar incorreto (deve terminar com .apps.googleusercontent.com)")
    else:
        print(f"✅ GOOGLE_CLIENT_ID: {settings.GOOGLE_CLIENT_ID[:30]}...")
    
    # Verificar Client Secret
    if not settings.GOOGLE_CLIENT_SECRET:
        errors.append("❌ GOOGLE_CLIENT_SECRET não está configurado")
    elif not settings.GOOGLE_CLIENT_SECRET.startswith('GOCSPX-'):
        warnings.append("⚠️  GOOGLE_CLIENT_SECRET pode estar incorreto (deve começar com GOCSPX-)")
    else:
        print(f"✅ GOOGLE_CLIENT_SECRET: {settings.GOOGLE_CLIENT_SECRET[:10]}...")
    
    # Verificar Redirect URI
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    print(f"✅ GOOGLE_REDIRECT_URI: {redirect_uri}")
    
    # Verificar formato do Redirect URI
    if not redirect_uri.startswith('http://') and not redirect_uri.startswith('https://'):
        errors.append("❌ GOOGLE_REDIRECT_URI deve começar com http:// ou https://")
    
    if 'localhost' in redirect_uri and not redirect_uri.startswith('http://'):
        warnings.append("⚠️  Para localhost, use http:// (não https://)")
    
    # Verificar se o caminho está correto
    expected_path = "/api/v1/auth/oauth/google/callback"
    if expected_path not in redirect_uri:
        errors.append(f"❌ GOOGLE_REDIRECT_URI deve conter: {expected_path}")
        errors.append(f"   URI atual: {redirect_uri}")
    
    print("\n" + "="*60)
    print("📋 CHECKLIST DO GOOGLE CLOUD CONSOLE")
    print("="*60)
    print("\n1. Acesse: https://console.cloud.google.com/apis/credentials")
    print("2. Selecione seu OAuth 2.0 Client ID")
    print("3. Verifique se está configurado:")
    print(f"\n   ✅ Authorized redirect URIs:")
    print(f"      {redirect_uri}")
    print("\n   ✅ Authorized JavaScript origins:")
    print("      http://localhost:8000")
    print("      http://localhost:3000")
    print("\n   ⚠️  IMPORTANTE: O redirect URI deve ser EXATAMENTE igual!")
    print("      (incluindo http/https, porta, e caminho completo)")
    
    print("\n" + "="*60)
    
    if errors:
        print("\n❌ ERROS ENCONTRADOS:")
        for error in errors:
            print(f"   {error}")
        return False
    
    if warnings:
        print("\n⚠️  AVISOS:")
        for warning in warnings:
            print(f"   {warning}")
    
    print("\n✅ Configuração básica parece correta!")
    print("\n💡 Se ainda tiver problemas:")
    print("   1. Verifique se o redirect URI no Google Console está EXATAMENTE igual")
    print("   2. Aguarde alguns minutos após alterar no Google Console (pode levar tempo para propagar)")
    print("   3. Limpe o cache do navegador")
    print("   4. Verifique se o OAuth consent screen está configurado")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = verify_oauth_config()
    sys.exit(0 if success else 1)






