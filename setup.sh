#!/bin/bash
echo "Setting up Echo Swarm environment..."

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install crewai crewai-tools langchain-groq chromadb duckduckgo-search

if [ ! -f .env ]; then
  echo "GROQ_API_KEY=your_key_here" > .env
  echo "Created .env file. Please edit it with your Groq API key."
fi

echo "Setup complete. Run ./run_echo.sh to start."
