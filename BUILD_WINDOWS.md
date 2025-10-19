# 🪟 Como gerar executável para Windows

## ⚠️ IMPORTANTE

O PyInstaller **NÃO faz cross-compilation**. Isso significa:
- Build no Linux → Gera executável Linux (.elf)
- Build no Windows → Gera executável Windows (.exe)
- Build no macOS → Gera executável macOS (.app)

## Opção 1: Build direto no Windows (Recomendado)

### Pré-requisitos
1. Instale Python 3.8+ no Windows
2. Clone o repositório no Windows

### Passos

```powershell
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
.\venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt
pip install pyinstaller

# 4. Gerar executável
pyinstaller --clean RiverCleanup.spec
```

O executável estará em: `dist\RiverCleanup\RiverCleanup.exe`

## Opção 2: Usando WSL + Windows

Se você tem WSL2 instalado:

1. **No WSL (Linux):**
   ```bash
   # Desenvolva normalmente
   python main.py
   ```

2. **No Windows (PowerShell/CMD):**
   ```powershell
   # Clone o projeto em uma pasta Windows
   cd C:\Users\SeuNome\projetos\gamejam25
   
   # Instale Python Windows
   python -m venv venv
   .\venv\Scripts\activate
   pip install pygame pyinstaller
   
   # Gere o build
   pyinstaller --clean RiverCleanup.spec
   ```

## Opção 3: GitHub Actions (Automático)

Crie `.github/workflows/build.yml`:

```yaml
name: Build Windows EXE

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build with PyInstaller
      run: |
        pyinstaller --clean RiverCleanup.spec
    
    - name: Create ZIP
      run: |
        Compress-Archive -Path dist/RiverCleanup -DestinationPath RiverCleanup-Windows.zip
    
    - name: Upload Release
      uses: actions/upload-artifact@v3
      with:
        name: RiverCleanup-Windows
        path: RiverCleanup-Windows.zip
```

## Opção 4: Máquina Virtual

1. Instale VirtualBox ou VMware
2. Crie uma VM com Windows 10/11
3. Instale Python e siga os passos da Opção 1

## Opção 5: Wine (Não Recomendado)

```bash
# Instalar Wine
sudo apt install wine wine64

# Instalar Python Windows via Wine
# (Processo complexo e propenso a erros)
```

❌ **Não recomendado**: Wine tem muitos problemas com PyInstaller.

## 📝 Spec File para Windows

O arquivo `RiverCleanup.spec` já está configurado para funcionar no Windows:

```python
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RiverCleanup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Sem console do CMD
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico'  # Adicione um ícone se desejar
)
```

## 🎯 Recomendação Final

**Para distribuir no Windows:**
1. Use uma máquina Windows real (física ou VM)
2. Instale Python + PyInstaller
3. Execute o build
4. Teste o executável
5. Distribua o ZIP completo

**Ou use GitHub Actions** para automatizar tudo!

## 🔧 Adicionar Ícone (Opcional)

```bash
# No Windows, adicione ao .spec:
exe = EXE(
    ...,
    icon='assets/game_icon.ico'
)
```

Você pode converter PNG para ICO usando:
- https://convertio.co/png-ico/
- Ou: `pip install pillow` + script Python
