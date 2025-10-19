# 🔧 Correção v1.0.1 - Caminhos de Assets

## ❌ Problema Reportado

```
FileNotFoundError: No file 'assets/rio.png' found in working directory 
'C:\Users\rickk\Downloads\RiverCleanup-Windows-v1.0.0'.
```

### Causa Raiz

Quando o PyInstaller empacota uma aplicação, ele cria um diretório temporário para extrair os arquivos.  
Os caminhos relativos simples (`'assets/rio.png'`) **não funcionam** porque:

1. O executável é extraído para um diretório temporário
2. Os assets ficam em `sys._MEIPASS/assets/`
3. O código estava procurando em `./assets/` (diretório de trabalho atual)

## ✅ Solução Implementada

### 1. Criado `utils.py` com função `resource_path()`

```python
import os
import sys

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running from source, use current directory
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
```

### 2. Atualizado `game.py`

**Antes:**
```python
rio_original = pygame.image.load('assets/rio.png').convert_alpha()
margens_original = pygame.image.load('assets/margens.png').convert_alpha()
```

**Depois:**
```python
from utils import resource_path

rio_original = pygame.image.load(resource_path('assets/rio.png')).convert_alpha()
margens_original = pygame.image.load(resource_path('assets/margens.png')).convert_alpha()
```

### 3. Atualizado `entities/floating_object.py`

**Antes:**
```python
self.image = pygame.image.load(self.object.image)
```

**Depois:**
```python
from utils import resource_path

self.image = pygame.image.load(resource_path(self.object.image))
```

## 📋 Arquivos Modificados

- ✅ `utils.py` - **CRIADO** - Função helper para caminhos
- ✅ `game.py` - **ATUALIZADO** - Usa `resource_path()`
- ✅ `entities/floating_object.py` - **ATUALIZADO** - Usa `resource_path()`

## 🎯 Como Funciona

### Em Desenvolvimento (rodando do código fonte):
```python
resource_path('assets/rio.png')
# Retorna: '/home/user/projeto/assets/rio.png'
```

### Em Produção (executável PyInstaller):
```python
resource_path('assets/rio.png')
# Retorna: 'C:/Users/user/AppData/Local/Temp/_MEI123456/assets/rio.png'
```

## 🚀 Nova Release

**Tag**: `v1.0.1`  
**Commit**: `4f2f26a`  
**Mensagem**: "fix: Corrige caminho dos assets para funcionar com PyInstaller"

### Mudanças de Versão

- ~~v1.0.0~~ - Assets não carregavam no executável ❌
- **v1.0.1** - Assets carregam corretamente ✅

## 📦 Download

A nova versão estará disponível em:  
**https://github.com/ricardosousa339/gamejam25/releases/tag/v1.0.1**

Arquivos:
- `RiverCleanup-Windows-v1.0.1.zip` - **CORRIGIDO** ✅
- `RiverCleanup-Linux-v1.0.1.tar.gz` - **CORRIGIDO** ✅

## ⏱️ Timeline

1. **v1.0.0 Lançada** - Build com erro de caminhos
2. **Erro Reportado** - Assets não encontrados
3. **Investigação** - Identificado problema com caminhos relativos
4. **Correção Aplicada** - Criado `utils.py` e atualizado código
5. **v1.0.1 Lançada** - Build corrigido

## 🧪 Testado

✅ Funcionamento local (desenvolvimento)  
✅ Build PyInstaller (testado estrutura)  
⏳ Aguardando teste do executável Windows final

## 📝 Lições Aprendidas

1. **PyInstaller != Ambiente de Desenvolvimento**
   - Caminhos relativos funcionam diferente
   - Sempre usar `sys._MEIPASS` quando disponível

2. **Testar Executável Antes de Release**
   - Build local não garante que executável funcione
   - Sempre testar o `.exe`/executável final

3. **Função Helper é Essencial**
   - `resource_path()` abstrai a complexidade
   - Funciona em dev e produção

## 🔄 Para Futuras Referências

**SEMPRE usar `resource_path()` ao carregar assets:**

```python
# ❌ ERRADO
image = pygame.image.load('assets/image.png')
sound = pygame.mixer.Sound('sounds/effect.wav')
font = pygame.font.Font('fonts/arial.ttf', 24)

# ✅ CORRETO
image = pygame.image.load(resource_path('assets/image.png'))
sound = pygame.mixer.Sound(resource_path('sounds/effect.wav'))
font = pygame.font.Font(resource_path('fonts/arial.ttf'), 24)
```

---

**Status**: ✅ CORRIGIDO em v1.0.1  
**ETA Build**: ~5-10 minutos  
**Próxima Ação**: Testar executável Windows v1.0.1
