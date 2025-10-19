# Sistema de Animação de Splash

## [2025-10-19] - Splash ao Capturar Lixo

### ✅ Funcionalidade Implementada

Quando o pegador captura um lixo, uma **animação de splash** é exibida no ponto de colisão, simulando a água sendo perturbada.

---

## 🎯 Motivação

**Antes:**
- Pegador colide com lixo
- Lixo é capturado instantaneamente
- ❌ Sem feedback visual da captura
- ❌ Transição abrupta

**Depois:**
- Pegador colide com lixo
- **Animação de splash aparece no ponto de colisão**
- Lixo é capturado
- ✅ Feedback visual imediato
- ✅ Efeito "juicy" de água

---

## 🎨 Sprite e Animação

### Spritesheet
- **Arquivo**: `assets/splash.png`
- **Dimensões**: 64x256 pixels
- **Layout**: 1x4 vertical (4 frames empilhados)
- **Frame size**: 64x64 pixels cada

### Timing
```
Frame 0: 0-100ms   (inicial - pequeno splash)
Frame 1: 100-200ms (médio splash)
Frame 2: 200-300ms (splash completo)
Frame 3: 300-400ms (dissipando)
Total: 400ms (0.4 segundos)
```

---

## 🔧 Implementação

### Nova Entidade: `entities/splash.py`

```python
class Splash(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Carrega spritesheet 64x256
        # Extrai 4 frames de 64x64
        # Posiciona no ponto (x, y)
        self.frame_duration = 100  # 100ms por frame
        self.animation_complete = False
```

### Método `update()`
```python
def update(self):
    # Incrementa timer a cada frame (~16ms @ 60 FPS)
    self.frame_timer += 16
    
    # A cada 100ms, avança para próximo frame
    if self.frame_timer >= self.frame_duration:
        self.current_frame += 1
        
        # Se chegou no frame 4, remove sprite
        if self.current_frame >= 4:
            self.kill()
```

### Auto-destruição
- Após exibir todos os 4 frames (400ms)
- Chama `self.kill()` automaticamente
- Remove-se do `all_sprites` group

---

## 🎮 Integração no Jogo

### Modificação em `pegador.py`

#### Método `capture_trash()` agora retorna `bool`:
```python
def capture_trash(self, trash):
    if self.captured_trash is None and self.state == PegadorState.DESCENDING:
        self.captured_trash = trash
        trash.is_captured = True
        self.state = PegadorState.ASCENDING
        return True  # ← Indica que capturou (cria splash)
    return False
```

### Modificação em `game.py`

#### Detecção de colisão com criação de splash:
```python
# Antes
self.pegador.capture_trash(trash)

# Depois
if self.pegador.capture_trash(trash):
    # Criar splash no ponto de colisão
    splash = Splash(trash.rect.centerx, trash.rect.centery)
    self.all_sprites.add(splash)
```

---

## 📍 Posicionamento

O splash é criado **exatamente onde o lixo estava**:
```python
splash = Splash(trash.rect.centerx, trash.rect.centery)
```

### Coordenadas
- **X**: Centro horizontal do lixo
- **Y**: Centro vertical do lixo
- **Z-order**: Renderizado na ordem de adição ao `all_sprites`

---

## 🎬 Fluxo de Animação

```
1. Pegador mergulha (DESCENDING)
   ║
   ║  [LIXO]
   ↓
2. Colisão detectada
   ║
   ║  collision_rect ∩ trash.rect
   ↓
3. Captura + Splash
   ║
   ║  • pegador.capture_trash(trash) → True
   ║  • Splash(x, y) criado
   ║  • all_sprites.add(splash)
   ↓
4. Animação de splash (400ms)
   ║
   ║  Frame 0 (0-100ms)    💧
   ║  Frame 1 (100-200ms)  💦
   ║  Frame 2 (200-300ms)  💦💦
   ║  Frame 3 (300-400ms)  💧
   ↓
5. Auto-remove
   ║
   ║  splash.kill()
   ↓
6. Pegador retorna (ASCENDING)
   ║
   ║  [LIXO] preso na rede
   ↓
7. Margem + 1 segundo de exibição
```

---

## ⚙️ Configuração

### Velocidade da Animação
Para ajustar a velocidade do splash, modifique em `splash.py`:

```python
# Mais rápido (200ms total)
self.frame_duration = 50  # 50ms por frame

# Atual (400ms total)
self.frame_duration = 100  # 100ms por frame

# Mais lento (800ms total)
self.frame_duration = 200  # 200ms por frame
```

### Tamanho do Splash
O sprite já está em 64x64. Para escalar:

```python
# Em splash.py, após extrair frames
scale_factor = 1.5  # 150% maior
for i in range(4):
    frame = spritesheet.subsurface(...)
    frame = pygame.transform.smoothscale(
        frame, 
        (int(64 * scale_factor), int(64 * scale_factor))
    )
    self.frames.append(frame)
```

---

## 🔄 Ciclo de Vida do Splash

```
CRIAÇÃO (game.py)
    ↓
Splash.__init__()
    ↓
all_sprites.add(splash)
    ↓
LOOP (60 FPS)
    ↓
splash.update() × ~25 frames
    ↓
FRAME 4 ATINGIDO (400ms)
    ↓
splash.kill()
    ↓
REMOVIDO DE all_sprites
    ↓
GARBAGE COLLECTED
```

---

## 📊 Performance

### Custo por Splash
- **Memória**: ~64KB (spritesheet compartilhado)
- **CPU**: Mínimo (apenas frame increment)
- **Duração**: 400ms (~25 frames @ 60 FPS)

### Múltiplos Splashes
- Cada captura cria 1 splash independente
- Máximo teórico: ~15 splashes simultâneos (se capturar 1 a cada 400ms durante 6s)
- Na prática: 1-2 splashes ativos de cada vez

---

## 🎨 Camadas de Renderização

```
┌──────────────────────────────┐
│ rio.png (animado, fundo)     │
├──────────────────────────────┤
│ FloatingObjects (lixos)      │
├──────────────────────────────┤
│ Crocodile (jacaré)           │
├──────────────────────────────┤
│ Pegador (rede)               │
├──────────────────────────────┤
│ SPLASH (💦 animação)         │ ← NOVO
├──────────────────────────────┤
│ margens.png (estático, topo) │
└──────────────────────────────┘
```

O splash aparece **sobre** o pegador e lixo, mas **abaixo** das margens.

---

## 🐛 Considerações

### Por que não criar splash no pegador?
```python
# ❌ ERRADO - Pegador não tem acesso ao all_sprites
class Pegador:
    def capture_trash(self, trash):
        splash = Splash(...)  # Como adicionar ao all_sprites?
```

**Solução**: Criar splash no `game.py` que gerencia os sprite groups.

### Sincronização com Captura
O splash é criado **no mesmo frame** da captura:
```python
if self.pegador.capture_trash(trash):  # Captura acontece
    splash = Splash(...)                # Splash criado imediatamente
    self.all_sprites.add(splash)        # Visível no próximo render
```

---

## 🎯 Resultado

A adição do splash:
- ✅ **Feedback visual imediato** - Vê exatamente onde capturou
- ✅ **Efeito "juicy"** - Jogo parece mais vivo
- ✅ **Satisfação aumentada** - Coleta parece mais impactante
- ✅ **Clareza** - Momento exato de captura fica óbvio
- ✅ **Polimento** - Animação profissional

**Impacto no Gameplay:**
- Não afeta mecânicas (é puramente visual)
- Não bloqueia ações do jogador
- Auto-gerenciado (sem lógica adicional)

---

## 📝 Arquivos Modificados

1. **`entities/splash.py`** (NOVO)
   - Classe Splash completa
   - Sistema de animação de 4 frames
   - Auto-destruição após 400ms

2. **`entities/__init__.py`**
   - Adicionado: `from .splash import Splash`

3. **`entities/pegador.py`**
   - Modificado: `capture_trash()` retorna `bool`
   - Retorna `True` quando captura com sucesso

4. **`game.py`**
   - Adicionado: `from entities.splash import Splash`
   - Modificado: Criação de splash ao capturar lixo

---

## ✅ Validações

- [x] Splash aparece ao capturar lixo
- [x] Animação roda pelos 4 frames
- [x] Splash desaparece após 400ms
- [x] Posicionamento correto (centro do lixo)
- [x] Múltiplos splashes funcionam simultaneamente
- [x] Sem vazamento de memória (auto-remove)
- [x] Performance mantida (60 FPS)
- [x] Sem erros de compilação
- [x] Compatível com sistema de captura existente

---

**Data:** 2025-10-19  
**Versão:** 1.6.0 (Splash Animation)  
**Status:** ✅ CONCLUÍDO E TESTADO

💦💦💦
