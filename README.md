# OpenAI to Gemini Converter

This project is a Python tool designed to process and convert ChatGPT data exports into more usable formats. It takes the `conversations.json` file from a ChatGPT export and transforms it into a human-readable `.txt` file and a structured `.json` file.

## Usage

To run the conversion, you'll need Python 3 installed.

1.  **Make the script executable (if it's not already):**
    ```bash
    chmod +x scripts/run.sh
    ```

2.  **Execute the script with the path to your ChatGPT export directory:**
    ```bash
    ./scripts/run.sh /path/to/your/chatgpt-export
    ```

This will:
*   Create a Python virtual environment in a `venv` directory.
*   Install any dependencies from `requirements.txt`.
*   Run the `scripts/process_chatgpt_data.py` script.
*   Generate `chatgpt_export.txt` and `chatgpt_export.json` in the project root.
