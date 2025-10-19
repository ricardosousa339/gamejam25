# 🚀 Guia Rápido: Build Automático com GitHub Actions

## O que é?

O GitHub Actions irá **automaticamente** gerar executáveis para Windows e Linux sempre que você criar uma nova versão (tag).

## Como Usar

### 1. Configuração Inicial (Uma Vez)

O arquivo `.github/workflows/build.yml` já está criado! ✅

### 2. Criar uma Nova Release

Quando quiser lançar uma nova versão:

```bash
# 1. Commit suas alterações
git add .
git commit -m "Versão 1.0.0 pronta"

# 2. Criar tag com a versão
git tag v1.0.0

# 3. Fazer push do código E da tag
git push
git push --tags
```

### 3. Aguardar o Build

1. Vá para o GitHub: `https://github.com/ricardosousa339/gamejam25/actions`
2. Você verá o workflow "Build Windows Release" em execução
3. Aguarde ~5-10 minutos (builds automáticos levam um tempo)

### 4. Baixar os Executáveis

Quando o build terminar:

**Opção A: Via Actions (Artifacts)**
1. Clique no workflow concluído
2. Role até "Artifacts"
3. Baixe:
   - `RiverCleanup-Windows.zip`
   - `RiverCleanup-Linux.tar.gz`

**Opção B: Via Releases (Automático)**
1. Vá para: `https://github.com/ricardosousa339/gamejam25/releases`
2. Clique na release (v1.0.0)
3. Baixe os arquivos em "Assets"

## Execução Manual (Sem Tag)

Se quiser rodar o build sem criar uma tag:

1. Vá para: `https://github.com/ricardosousa339/gamejam25/actions`
2. Clique em "Build Windows Release"
3. Clique no botão "Run workflow" (canto direito)
4. Selecione a branch e clique em "Run workflow"

## Estrutura dos Arquivos Gerados

### Windows
```
RiverCleanup-Windows-v1.0.0.zip
└── RiverCleanup/
    ├── RiverCleanup.exe
    └── _internal/
        └── assets/
```

### Linux
```
RiverCleanup-Linux-v1.0.0.tar.gz
└── RiverCleanup/
    ├── RiverCleanup
    └── _internal/
        └── assets/
```

## Versionamento Semântico

Use versionamento semântico para suas tags:

- `v1.0.0` - Primeira release
- `v1.0.1` - Bug fixes
- `v1.1.0` - Novas features
- `v2.0.0` - Mudanças que quebram compatibilidade

Exemplos:
```bash
git tag v1.0.0   # Primeira versão
git tag v1.0.1   # Correção de bug
git tag v1.1.0   # Nova funcionalidade
git tag v2.0.0   # Mudança grande
```

## Troubleshooting

### Build Falhou
1. Verifique os logs no GitHub Actions
2. Problemas comuns:
   - Dependência faltando em `requirements.txt`
   - Erro no arquivo `.spec`
   - Asset não encontrado

### Tag Duplicada
```bash
# Deletar tag local e remota
git tag -d v1.0.0
git push --delete origin v1.0.0

# Criar nova tag
git tag v1.0.0
git push --tags
```

### Testar Localmente Antes

```bash
# Linux (seu ambiente atual)
./build.sh

# Simular o que o GitHub Actions fará
pyinstaller --clean RiverCleanup.spec
```

## Customização

### Mudar Python Version
Edite `.github/workflows/build.yml`:
```yaml
python-version: '3.11'  # Mude para 3.12, 3.10, etc
```

### Adicionar macOS Build
Adicione ao workflow:
```yaml
  build-macos:
    runs-on: macos-latest
    # ... (similar aos outros)
```

### Notificações
Adicione ao final do workflow:
```yaml
    - name: Notify Discord
      uses: sarisia/actions-status-discord@v1
      if: always()
      with:
        webhook: ${{ secrets.DISCORD_WEBHOOK }}
```

## Vantagens

✅ **Automático** - Sem precisar de máquina Windows
✅ **Consistente** - Mesmo ambiente sempre
✅ **Rápido** - Builds em paralelo
✅ **Grátis** - GitHub Actions é grátis para repos públicos
✅ **Releases** - Cria releases automaticamente

## Exemplo de Workflow Completo

```bash
# 1. Fazer mudanças
vim game.py

# 2. Testar localmente
python main.py

# 3. Commit
git add .
git commit -m "Adiciona novo recurso"

# 4. Push
git push

# 5. Quando pronto para release
git tag v1.0.0
git push --tags

# 6. Aguardar build automático
# 7. Baixar executáveis da página de Releases
# 8. Distribuir!
```

## Links Úteis

- [Suas Actions](https://github.com/ricardosousa339/gamejam25/actions)
- [Suas Releases](https://github.com/ricardosousa339/gamejam25/releases)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
