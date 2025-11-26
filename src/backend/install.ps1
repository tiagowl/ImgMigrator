# Script de instalação para Windows PowerShell
# Este script instala as dependências usando apenas wheels pré-compilados

Write-Host "Instalando dependências do Cloud Migrate Backend..." -ForegroundColor Green

# Atualizar pip
Write-Host "`nAtualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instalar dependências usando apenas wheels (sem compilação)
Write-Host "`nInstalando dependências (apenas wheels pré-compilados)..." -ForegroundColor Yellow
python -m pip install --only-binary :all: -r requirements.txt

# Se ainda houver problemas, tentar instalar pydantic-core separadamente
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nTentando instalar pydantic-core separadamente..." -ForegroundColor Yellow
    python -m pip install --only-binary :all: pydantic-core==2.14.6
    python -m pip install --only-binary :all: -r requirements.txt
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ Dependências instaladas com sucesso!" -ForegroundColor Green
} else {
    Write-Host "`n✗ Erro ao instalar dependências." -ForegroundColor Red
    Write-Host "`nAlternativa: Instale Rust manualmente de https://rustup.rs/" -ForegroundColor Yellow
    Write-Host "Ou use uma versão mais antiga do pydantic que não requer compilação." -ForegroundColor Yellow
}






