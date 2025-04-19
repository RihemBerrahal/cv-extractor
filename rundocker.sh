#!/bin/bash

echo "🔄 Starting CV Extractor with Ollama..."

# Start Docker containers in detached mode
docker-compose up -d

# Wait for the Ollama service to initialize
echo "⏳ Waiting for Ollama service to be ready..."
sleep 15

# Pull models into the Ollama container
for model in llama3 mistral phi; do
    echo "📦 Pulling model: $model"
    docker-compose exec ollama ollama pull $model
done

echo "✅ CV Extractor is now running at http://localhost:5000"
