# ✅ Checklist de Build - River Cleanup Game

## Status do Build Atual

🎯 **Build Linux**: ✅ Completo (46MB)
- Localização: `dist/RiverCleanup/`
- Executável: `RiverCleanup` (Linux)
- Assets incluídos: ✅
- Bibliotecas incluídas: ✅

🪟 **Build Windows**: ⚠️ Requer build no Windows
- Ver: [BUILD_WINDOWS.md](BUILD_WINDOWS.md)

## Arquivos Criados

### Documentação
- ✅ `BUILD_INSTRUCTIONS.md` - Instruções gerais de build
- ✅ `BUILD_WINDOWS.md` - Guia específico para Windows
- ✅ `README.md` - Atualizado com seção de build
- ✅ `build.sh` - Script automatizado de build

### Configuração
- ✅ `RiverCleanup.spec` - Configuração PyInstaller (já existia)
- ✅ `requirements.txt` - Dependências Python

### Build Atual
- ✅ `dist/RiverCleanup/` - Diretório de distribuição
  - ✅ Executável principal
  - ✅ `_internal/assets/` - Todos os assets incluídos
  - ✅ Bibliotecas Pygame incluídas

## Para Gerar Build Windows (.exe)

### Opção Rápida: GitHub Actions
1. Crie `.github/workflows/build.yml`
2. Faça push com tag: `git tag v1.0.0 && git push --tags`
3. O executável será gerado automaticamente

### Opção Manual: Computador Windows
1. Clone o projeto no Windows
2. Instale Python 3.8+
3. Execute:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   pip install pyinstaller
   pyinstaller --clean RiverCleanup.spec
   ```

## Próximos Passos para Distribuição

### Antes de Distribuir
- [ ] Testar executável em máquina limpa (sem Python)
- [ ] Adicionar ícone personalizado (opcional)
- [ ] Criar arquivo LEIAME.txt com instruções
- [ ] Testar em diferentes versões do Windows (7, 10, 11)

### Assets Opcionais
- [ ] Adicionar ícone do jogo (.ico)
- [ ] Incluir README em texto simples
- [ ] Adicionar arquivo de licença

### Melhorias Futuras
- [ ] Build de um único arquivo (`--onefile`)
- [ ] Assinatura digital do executável
- [ ] Instalador com NSIS ou Inno Setup
- [ ] Auto-updater

## Comandos Úteis

### Build Rápido
```bash
./build.sh
```

### Limpar Builds Antigos
```bash
rm -rf build/ dist/
```

### Testar Build
```bash
cd dist/RiverCleanup
./RiverCleanup  # Linux
# ou
RiverCleanup.exe  # Windows
```

### Criar ZIP para Distribuição
```bash
cd dist
zip -r RiverCleanup-v1.0.0.zip RiverCleanup/
```

## Tamanho do Build

- **Total**: ~46MB
- **Executável**: ~4MB
- **Bibliotecas**: ~40MB
- **Assets**: ~2MB

## Notas Importantes

⚠️ **Cross-Platform**
- PyInstaller NÃO faz cross-compilation
- Build Linux → Executável Linux
- Build Windows → Executável Windows

⚠️ **Distribuição**
- Sempre distribua a pasta COMPLETA
- Não distribua apenas o executável
- O executável precisa da pasta `_internal/`

⚠️ **Antivírus**
- Executáveis PyInstaller podem ser flagged como falso positivo
- Solução: Assinatura digital ou submeter para whitelist

## Recursos

- [PyInstaller Docs](https://pyinstaller.org/en/stable/)
- [Pygame Bundling](https://www.pygame.org/wiki/Deployment)
- [GitHub Actions Examples](https://github.com/actions/starter-workflows)
