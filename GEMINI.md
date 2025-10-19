# Gemini Code Assistant Context

## Project Overview

This project is a Python tool designed to process and convert ChatGPT data exports into more usable formats. It takes the `conversations.json` file from a ChatGPT export and transforms it into a human-readable `.txt` file and a structured `.json` file.

The main logic is contained in `scripts/process_chatgpt_data.py`, and the `run.sh` script provides a convenient way to set up the environment and execute the conversion.

## Building and Running

This is a Python project. To run it, you'll need Python 3 installed.

### Running the Conversion

The primary way to run the conversion is using the `run.sh` script.

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

### Manual Execution

You can also run the Python script directly:

1.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    ```bash
    python scripts/process_chatgpt_data.py /path/to/your/chatgpt-export --txt output.txt --json output.json
    ```

## Development Conventions

*   The project uses standard Python with the `argparse` library for command-line argument parsing.
*   The `run.sh` script is the recommended way to execute the project, simplifying setup and execution.
*   The project is structured with a clear separation between the main script (`scripts/process_chatgpt_data.py`) and the execution wrapper (`scripts/run.sh`).
