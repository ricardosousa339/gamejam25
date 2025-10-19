# Instruções de Build - River Cleanup Game

## 📦 Build para Windows (.exe)

### Opção 1: Build Automático (Recomendado)

O projeto já está configurado com PyInstaller. Para gerar o executável:

```bash
# Ative o ambiente virtual
source venv/bin/activate

# Execute o build
pyinstaller --clean RiverCleanup.spec
```

O executável estará em: `dist/RiverCleanup/`

### Opção 2: Build Manual

Se precisar reconfigurar:

```bash
pyinstaller --onedir \
    --windowed \
    --name RiverCleanup \
    --add-data "assets:assets" \
    main.py
```

## 📁 Estrutura do Build

```
dist/RiverCleanup/
├── RiverCleanup.exe      # Executável principal (Windows)
├── RiverCleanup          # Executável principal (Linux)
└── _internal/            # Bibliotecas e assets necessários
    ├── assets/           # Imagens e recursos do jogo
    │   ├── rio.png
    │   ├── margens.png
    │   ├── crocodilo.png
    │   └── lixo/
    └── [bibliotecas.dll/so]
```

## 🎮 Distribuição

Para distribuir o jogo:

1. Comprima toda a pasta `dist/RiverCleanup/` em um arquivo ZIP
2. **IMPORTANTE**: O usuário deve extrair TUDO antes de executar
3. O executável precisa estar junto com a pasta `_internal/`

### Testando no Windows

Se você estiver compilando no Linux/WSL para Windows:

1. O executável gerado é para Linux
2. Para compilar para Windows, você precisa:
   - Executar o PyInstaller no Windows, OU
   - Usar Wine (não recomendado), OU
   - Usar uma VM Windows

## 🔧 Dependências

Certifique-se de que o `requirements.txt` está atualizado:

```
pygame>=2.5.0
pyinstaller>=6.0.0
```

## ⚠️ Observações

- **Build Cross-Platform**: PyInstaller gera executáveis apenas para o SO atual
- **Tamanho**: O executável final terá ~30-50MB devido às bibliotecas do Pygame
- **Antivírus**: Alguns antivírus podem alertar sobre executáveis PyInstaller (falso positivo)
- **Console**: O build está configurado como `--windowed` (sem console)

## 🐛 Troubleshooting

### Assets não encontrados
- Verifique se a linha `datas=[('assets', 'assets')]` está no `.spec`
- Confirme que a pasta `assets/` existe no diretório raiz

### Erro ao executar
- Certifique-se de que toda a pasta `_internal/` está presente
- Verifique se todas as DLLs necessárias estão incluídas

### Build muito grande
- Use `--onefile` para um único arquivo (mais lento ao iniciar)
- Remova assets não utilizados antes do build
