#!/bin/bash

echo "Setting up Multi-Agent LLM System..."

# Check if python3-venv is installed
if ! dpkg -l | grep -q python3-venv; then
    echo "Installing python3-venv..."
    sudo apt update
    sudo apt install -y python3-venv python3-pip
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ ! -d "venv" ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment template
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
else
    echo "⚠️  .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys: nano .env"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python main.py"
echo ""