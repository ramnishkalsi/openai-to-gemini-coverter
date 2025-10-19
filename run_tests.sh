#!/bin/bash

# --- Configuration ---
VENV_DIR="venv"

# --- Script Start ---
set -e # Exit immediately if a command exits with a non-zero status.

# 1. Virtual Environment Setup: Activate the venv.
if [ ! -d "$VENV_DIR" ]; then
  echo "🐍 Creating Python virtual environment in './$VENV_DIR'..."
  python3 -m venv "$VENV_DIR"
else
  echo "🐍 Virtual environment already exists."
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# 2. Run Tests
python -m unittest discover -s tests
