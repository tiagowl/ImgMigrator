# Guia de Instalação - Resolvendo Problemas com Rust

## Problema

O `pydantic-core` requer Rust para compilação, mas o Cargo não está no PATH do sistema.

## Soluções

### Solução 1: Instalar Rust (Recomendado para produção)

1. Baixe e instale Rust de: https://rustup.rs/
2. Reinicie o terminal/PowerShell
3. Verifique a instalação:
   ```powershell
   cargo --version
   ```
4. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```

### Solução 2: Usar requirements-simple.txt (Versões com wheels)

O arquivo `requirements-simple.txt` contém versões que têm wheels pré-compilados disponíveis:

```powershell
pip install -r requirements-simple.txt
```

**Nota:** Este arquivo usa versões mais recentes que têm wheels para Python 3.13.

### Solução 3: Usar ambiente virtual com Python 3.11 ou 3.12

Versões mais antigas do Python podem ter wheels pré-compilados disponíveis:

```powershell
# Criar ambiente virtual com Python 3.11
python3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Solução 4: Instalar apenas wheels pré-compilados

Tentar forçar instalação apenas de wheels:

```powershell
pip install --only-binary :all: -r requirements.txt
```

Se falhar, use a Solução 2 (requirements-simple.txt).

## Verificação

Após instalar, verifique:

```powershell
python -c "import fastapi; import pydantic; print('OK')"
```

Se não houver erros, a instalação foi bem-sucedida!

