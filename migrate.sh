#!/bin/bash

# --- Configuration ---
VENV_DIR="venv"
PYTHON_SCRIPT="scripts/replicate_chats.py"
REQUIREMENTS_FILE="requirements.txt"

# --- Script Start ---
set -e # Exit immediately if a command exits with a non-zero status.

# 1. Input Validation: Check if an input directory was provided.
if [ -z "$1" ]; then
  echo "❌ Error: No input directory specified."
  echo "Usage: ./migrate.sh /path/to/your/chatgpt-export-folder"
  exit 1
fi

INPUT_DIR="$1"
shift

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

MIGRATED_CONVERSATIONS=$(python "$PYTHON_SCRIPT" "$INPUT_DIR" "$@" | tee /dev/tty | grep "migrated_conversations=" | cut -d '=' -f 2)

OUTPUT_DIR="gemini_projects"
if [[ "$@" == *"--output_dir"* ]]; then
  OUTPUT_DIR=$(echo "$@" | awk -F'--output_dir ' '{print $2}' | awk '{print $1}')
fi

echo "----------------------------------------------------"
echo "✅ All done!"

echo ""
echo "SUMMARY"
echo "======="
echo "Input directory: $INPUT_DIR"
echo "Output directory: $OUTPUT_DIR"
echo "Conversations migrated: $MIGRATED_CONVERSATIONS"

# The script will automatically deactivate the venv upon exit.
