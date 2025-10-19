#!/bin/bash

# Script de build automatizado para River Cleanup Game
# Uso: ./build.sh

echo "🎮 River Cleanup - Build Script"
echo "================================"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ Erro: Execute este script do diretório raiz do projeto"
    exit 1
fi

# Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
if [ ! -d "venv" ]; then
    echo "❌ Erro: Ambiente virtual não encontrado. Execute: python -m venv venv"
    exit 1
fi

source venv/bin/activate

# Verificar se PyInstaller está instalado
if ! command -v pyinstaller &> /dev/null; then
    echo "📥 PyInstaller não encontrado. Instalando..."
    pip install pyinstaller
fi

# Limpar builds anteriores
echo "🧹 Limpando builds anteriores..."
rm -rf build/ dist/

# Executar build
echo "🔨 Gerando executável..."
pyinstaller --clean RiverCleanup.spec

# Verificar sucesso
if [ -f "dist/RiverCleanup/RiverCleanup" ] || [ -f "dist/RiverCleanup/RiverCleanup.exe" ]; then
    echo ""
    echo "✅ Build concluído com sucesso!"
    echo "📁 Localização: dist/RiverCleanup/"
    echo ""
    echo "Para distribuir:"
    echo "  1. Comprima a pasta dist/RiverCleanup/"
    echo "  2. Distribua o arquivo ZIP completo"
    echo ""
    
    # Mostrar tamanho
    SIZE=$(du -sh dist/RiverCleanup/ | cut -f1)
    echo "📊 Tamanho total: $SIZE"
    
    # Criar ZIP automático (opcional)
    read -p "Deseja criar um arquivo ZIP agora? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "📦 Criando ZIP..."
        cd dist
        zip -r RiverCleanup.zip RiverCleanup/
        cd ..
        echo "✅ Arquivo criado: dist/RiverCleanup.zip"
    fi
else
    echo "❌ Erro durante o build. Verifique os logs acima."
    exit 1
fi
