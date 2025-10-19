#!/bin/bash

# --- Configuration ---
VENV_DIR="venv"
PYTHON_SCRIPT="scripts/process_chatgpt_data.py"
REQUIREMENTS_FILE="requirements.txt"
DEFAULT_TXT_OUTPUT="chatgpt_export.txt"
DEFAULT_JSON_OUTPUT="chatgpt_export.json"

# --- Script Start ---
set -e # Exit immediately if a command exits with a non-zero status.

# 1. Input Validation: Check if an input directory was provided.
if [ -z "$1" ]; then
  echo "❌ Error: No input directory specified."
  echo "Usage: ./scripts/migrate.sh /path/to/your/chatgpt-export-folder"
  exit 1
fi

INPUT_DIR="$1"

# 2. Check if the input directory exists.
if [ ! -d "$INPUT_DIR" ]; then
    echo "❌ Error: The specified directory does not exist: $INPUT_DIR"
    exit 1
fi

# 3. Virtual Environment Setup: Create or activate the venv.
if [ ! -d "$VENV_DIR" ]; then
  echo "🐍 Creating Python virtual environment in './$VENV_DIR'..."
  python3 -m venv "$VENV_DIR"
else
  echo "🐍 Virtual environment already exists."
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# 4. Dependency Installation: Install requirements quietly.
if [ -f "$REQUIREMENTS_FILE" ]; then
  echo "📦 Installing dependencies from '$REQUIREMENTS_FILE'..."
  pip install -r "$REQUIREMENTS_FILE" -q # -q for quiet mode
else
    echo "👍 No '$REQUIREMENTS_FILE' found, skipping dependency installation."
fi

# 5. Execute the Python Script: Pass the input directory and output flags.
echo "🚀 Running the Python script to process your data..."
echo "----------------------------------------------------"

MIGRATED_CONVERSATIONS=$(python "$PYTHON_SCRIPT" "$INPUT_DIR" --txt "$DEFAULT_TXT_OUTPUT" --json "$DEFAULT_JSON_OUTPUT" | grep "migrated_conversations=" | cut -d '=' -f 2)

echo "----------------------------------------------------"
echo "✅ All done!"

echo ""
echo "SUMMARY"
echo "======="
echo "Input directory: $INPUT_DIR"
echo "Output files:"
echo "  - $DEFAULT_TXT_OUTPUT"
echo "  - $DEFAULT_JSON_OUTPUT"
echo "Conversations migrated: $MIGRATED_CONVERSATIONS"

# The script will automatically deactivate the venv upon exit.
