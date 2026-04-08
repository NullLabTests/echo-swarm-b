#!/bin/bash
# Echo Swarm — one-click setup for weak Linux daemon + Groq free tier

set -e

echo "🚀 Setting up Echo Swarm..."

# Create virtual env
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install everything
pip install crewai crewai-tools langchain-groq chromadb duckduckgo-search

echo "✅ Dependencies installed."

# Create .env
if [ ! -f .env ]; then
  cat > .env << EOT
GROQ_API_KEY=your_groq_key_here
# Optional: add SERPER_API_KEY=... later for better search
EOT
  echo "✅ .env created — edit it with your Groq key!"
fi

echo ""
echo "🎉 Setup complete!"
echo "Next: edit .env with your Groq API key, then run: ./run_echo.sh"
