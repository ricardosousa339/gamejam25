# Game Jam 2025 - River Cleanup

Um jogo de limpeza do rio onde você coleta objetos flutuantes e os coloca nas latas de lixo apropriadas.

## Estrutura do Projeto

```
gamejam25/
├── main.py              # Ponto de entrada do jogo
├── game.py              # Loop principal e lógica do jogo
├── config.py            # Configurações e constantes
├── utils.py             # Utilidades (resource_path para PyInstaller)
├── entities/            # Entidades do jogo
│   ├── __init__.py
│   ├── floating_object.py  # Objetos flutuando no rio
│   ├── pegador.py          # Sistema de pegador controlável
│   └── trash_can.py        # Latas de lixo
├── assets/              # Recursos gráficos
│   ├── rio.png          # Textura animada do rio
│   ├── margens.png      # Overlay estático das margens
│   ├── pegador_frente.png   # Sprite do pegador (vista frontal)
│   ├── pegador_lado.png     # Sprite do pegador (vista lateral)
│   └── lixo/            # Sprites dos diferentes tipos de lixo
├── RiverCleanup.spec   # Configuração do PyInstaller
├── build.sh            # Script de build automatizado
├── requirements.txt    # Dependências Python
├── PEGADOR_SYSTEM.md   # Documentação detalhada do sistema de pegador
└── README.md           # Este arquivo
```

## Instalação

1. Ative o ambiente virtual (se ainda não estiver ativo):
```bash
source venv/bin/activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

```bash
python main.py
```

## 📦 Build e Distribuição

### Gerar Executável

Para criar um executável distribuível:

```bash
# Usando o script automático
./build.sh

# Ou manualmente
pyinstaller --clean RiverCleanup.spec
```

O executável estará em `dist/RiverCleanup/`

### Documentação Completa

- **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)** - Instruções gerais de build
- **[BUILD_WINDOWS.md](BUILD_WINDOWS.md)** - Como gerar .exe para Windows

### Distribuição

Para distribuir o jogo:
1. Comprima toda a pasta `dist/RiverCleanup/`
2. Distribua o arquivo ZIP
3. ⚠️ O usuário deve extrair TUDO antes de executar

## Controles

### Pegador (Pool Net)
- **Setas Esquerda/Direita**: Move o pegador horizontalmente ao longo da margem inferior
- **Espaço (Segurar)**: Carrega a barra de força para determinar profundidade do mergulho
- **Espaço (Soltar)**: Mergulha o pegador para cima no rio para coletar lixo
- **ESC**: Sair do jogo

### Como Jogar
1. O pegador inicia na parte inferior da tela (margem)
2. Posicione o pegador horizontalmente usando as setas
3. Segure Espaço para carregar a força (barra verde/amarelo/vermelho)
4. Solte Espaço para mergulhar para cima - quanto mais força, mais profundo no rio
5. Colete o lixo flutuante colidindo com ele durante o mergulho
6. O pegador retorna automaticamente à margem inferior com o lixo
7. Ganhe pontos a cada coleta!

## Próximos Passos

- [ ] Integrar lixeiras para descarte correto (trash_can.py)
- [ ] Sistema de pontuação com penalidades por tipo errado
- [ ] Níveis de dificuldade crescente
- [ ] Obstáculos (crocodilo?)
- [ ] Power-ups e itens especiais
- [ ] Efeitos sonoros e música
- [ ] Menu inicial e tela de game over
- [ ] Animações de transição para o pegador
- [ ] Partículas de água durante mergulho
- [ ] Combos por múltiplas coletas consecutivas

## Características Atuais

✅ Loop de jogo básico funcionando
✅ Sistema de sprites com Pygame
✅ Objetos flutuantes que se movem com o rio
✅ **Sistema de pegador com controle horizontal**
✅ **Barra de força para controle de profundidade**
✅ **Captura de lixo durante mergulho**
✅ **Sistema de estados do pegador (ocioso, carregando, descendo, subindo)**
✅ **Lixo preso ao pegador durante retorno à margem**
✅ Sistema de pontuação (pontos por lixo coletado)
✅ Animação do rio com movimento paralaxo
✅ Diferentes tipos de lixo (plástico, metal, vidro, papel, misturado)
✅ Build automatizado com PyInstaller
