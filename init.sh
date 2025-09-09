#!/bin/bash

# Script to initialize the virtual environment and install dependencies

# Check if virtual environment exists
if [ ! -d "venv_py310_final" ]; then
    echo "Creating virtual environment..."
    python -m venv venv_py310_final
fi

# Activate virtual environment
source venv_py310_final/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete! To activate the virtual environment, run:"
echo "source venv_py310_final/bin/activate"