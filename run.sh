#!/bin/bash

echo "🚀 Starting CV Extractor Project..."

# 1. Check Python & pip
if ! command -v python3 &>/dev/null || ! command -v pip &>/dev/null; then
    echo "❌ Python3 and pip are required but not installed."
    exit 1
fi

# 2. Create and activate virtual environment
echo "🔧 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Check for Tesseract installation
if ! command -v tesseract &>/dev/null; then
    echo "❌ Tesseract OCR is not installed."
    echo "➡️ Please install it manually:"
    echo "   Ubuntu/Debian: sudo apt install tesseract-ocr"
    echo "   macOS: brew install tesseract"
    echo "   Windows: Download from https://github.com/tesseract-ocr/tesseract"
    exit 1
fi

# 5. Check Ollama
echo "🧠 Checking Ollama..."
if ! command -v ollama &>/dev/null; then
    echo "❌ Ollama not found. Please install it from https://ollama.com/download"
    exit 1
fi

# 6. Pull models
echo "⬇️ Pulling LLM models..."
ollama pull llama3
ollama pull mistral
ollama pull phi

# 7. Launch the web app
echo "🌐 Starting the web app..."
python app.py

echo "✅ App is running at http://localhost:5000"