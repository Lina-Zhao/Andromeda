#!/bin/bash

# Setup script for Week 1 project
# Run this script to set up the development environment

set -e  # Exit on error

echo "🚀 Setting up Week 1: LLM Inference Service"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Copy environment template if not exists
if [ ! -f ".env" ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration"
fi

# Create __init__.py files
echo "📁 Creating package structure..."
touch src/__init__.py
touch src/api/__init__.py
touch src/core/__init__.py
touch src/monitoring/__init__.py
touch tests/__init__.py

# Create directories
mkdir -p monitoring/grafana/dashboards
mkdir -p scripts
mkdir -p docs

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys and configuration"
echo "2. Start vLLM server: ./scripts/start_vllm.sh"
echo "3. Start API server: python -m src.main"
echo "4. View docs at: http://localhost:8080/docs"
echo ""
