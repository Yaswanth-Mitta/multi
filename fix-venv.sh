#!/bin/bash

# Fix virtual environment script
echo "🔧 Fixing virtual environment..."

# Remove corrupted venv
rm -rf venv

# Create new virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "✅ Virtual environment fixed!"
echo "Run: source venv/bin/activate"