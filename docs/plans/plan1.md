# Plan: Create a Tool to Replicate All ChatGPT Conversations for Gemini

**Objective:** Develop a Python script that automates the full replication of a ChatGPT data export. The script will parse all conversations and save them into a single, structured JSON file formatted specifically for compatibility with the Google Gemini API. This creates a complete, portable archive of all chat history.

---

## Step 1: Project Setup and Dependencies

Establish the project structure and define the single, minimal dependency.

1.  **Create the Directory Structure:**
    * Create a root project folder.
    * Inside the root, create a `scripts/` subfolder.

2.  **Create the `requirements.txt` file:**
    * In the **root** folder, create `requirements.txt`.
    * Add the library needed for potential future API interactions (though not for the conversion itself, it's good practice for a "Gemini environment" tool):
        ```text
        google-generativeai
        ```

---

## Step 2: Build the Core Python Script

Develop the main Python script to handle argument parsing and orchestrate the conversion process.

1.  **Create the Python File:**
    * Inside the `scripts/` directory, create a file named `replicate_chats.py`.

2.  **Import Necessary Libraries:**
    * Import `json`, `os`, and `argparse`.

3.  **Implement Argument Parsing:**
    * Use `argparse` to define the command-line interface.
    * The script must accept two arguments:
        * `input_dir`: A required positional argument for the path to the unzipped ChatGPT export folder.
        * `--output_file`: An optional argument for the name of the final JSON output file (e.g., `gemini_archive.json`).

---

## Step 3: Implement Full ChatGPT Data Parsing

This part focuses on robustly processing the entire `conversations.json` file.

1.  **Create a `process_chatgpt_export` function:**
    * This function takes `input_dir` as an argument.
    * It locates and opens `conversations.json`, handling any file-not-found errors.
    * It iterates through **every conversation object** in the main JSON array.
    * For each conversation, it calls a helper function (`parse_conversation`) to reconstruct its message history.
    * It collects the results from the helper function into a final list of all processed conversations.

2.  **Create a `parse_conversation` helper function:**
    * This function takes a single raw conversation object.
    * It reconstructs the chat chronologically by starting at the `current_node` and traversing backwards through its `parent` nodes.
    * It extracts the `title` of the conversation.
    * For each message node, it converts the ChatGPT format (`{"role": "assistant", "content": ...}`) to the Gemini API format (`{"role": "model", "parts": [{"text": ...}]}`). Note the role change from `assistant` to `model`.
    * The function returns a single dictionary representing the fully parsed and formatted conversation.

---

## Step 4: Implement Final Archive Generation

This step involves writing the processed data to a durable file.

1.  **Consolidate Data:**
    * The main script logic will hold the list of all Gemini-formatted conversations returned by `process_chatgpt_export`.

2.  **Write to JSON File:**
    * Use the `json` library to write the consolidated list to the specified output file.
    * The output should be a single JSON file containing a list of conversation objects. Each object will have a `title` and a `history` key, where `history` is the list of Gemini-formatted messages.
    * Ensure the output is "pretty-printed" (indented) for readability.

---

## Step 5: Create a User-Friendly Wrapper Script

Automate the environment setup and execution with a simple shell script.

1.  **Create `migrate.sh` in the root directory:**
    * This script will be the user's primary entry point.

2.  **Implement Wrapper Logic:**
    * Define paths to the virtual environment (`venv`), `requirements.txt`, and the Python script (`scripts/replicate_chats.py`).
    * Check for and create a `venv` if one does not exist.
    * Activate the `venv`.
    * Install dependencies quietly from `requirements.txt` using `pip install -r -q`.
    * Execute the Python script, passing along all command-line arguments (like the input directory and optional output file name) it received.
    * Provide clear success messages upon completion.