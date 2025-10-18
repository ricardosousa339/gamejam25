# Game Jam 2025 - River Cleanup

Um jogo de limpeza do rio onde você coleta objetos flutuantes e os coloca nas latas de lixo apropriadas.

## Estrutura do Projeto

```
gamejam25/
├── main.py              # Ponto de entrada do jogo
├── game.py              # Loop principal e lógica do jogo
├── config.py            # Configurações e constantes
├── entities/            # Entidades do jogo
│   ├── __init__.py
│   ├── floating_object.py  # Objetos flutuando no rio
│   └── trash_can.py        # Latas de lixo
├── requirements.txt     # Dependências Python
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

## Controles

- **Mouse Click**: Clique em um objeto flutuante para selecioná-lo
- **Mouse Move**: Arraste o objeto selecionado até uma lata de lixo
- **ESC**: Sair do jogo

## Próximos Passos

- [ ] Adicionar sprites/imagens para os objetos
- [ ] Implementar sistema de spawn automático de objetos
- [ ] Adicionar diferentes tipos de latas de lixo
- [ ] Sistema de pontuação com penalidades para lixo errado
- [ ] Efeitos sonoros e música
- [ ] Menu inicial e tela de game over
- [ ] Níveis de dificuldade crescente
- [ ] Partículas e efeitos visuais

## Características Atuais

✅ Loop de jogo básico funcionando
✅ Sistema de sprites com Pygame
✅ Objetos flutuantes que se movem com o rio
✅ Latas de lixo estáticas
✅ Sistema de seleção e arrasto de objetos
✅ Detecção de colisão entre objetos e latas
✅ Sistema de pontuação básico
✅ Efeito visual do rio com linhas de fluxo
