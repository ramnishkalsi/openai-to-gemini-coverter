import json
import os
import argparse
import re
import google.generativeai as genai
from typing import List, Dict, Any


def get_project_name(title: str) -> str:
    """Extracts the project name from the conversation title."""
    match = re.search(r"^(Project:|Project |\[Project\]) (.*)", title, re.IGNORECASE)
    if match:
        return match.group(2).strip()

    if ' - ' in title:
        return title.split(' - ')[0].strip()

    return "General"

def generate_summary(conversation: Dict[str, Any]) -> str:
    """Generates a summary of the conversation using the Gemini API."""
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️  GEMINI_API_KEY environment variable not set. Skipping summary generation.")
        return ""

    print(f"Generating summary for conversation: {conversation['title']}")
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        chat_history = "\n".join([f"{msg['role']}: {msg['parts'][0]['text']}" for msg in conversation['history']])
        prompt = f"Please provide a one-paragraph summary of the following conversation:\n\n{chat_history}"
        response = model.generate_content(prompt)
        summary = response.text
        print(f"Summary for '{conversation['title']}': {summary}")
        return summary
    except Exception as e:
        print(f"Could not generate summary for conversation '{conversation['title']}': {e}")
        return ""

def parse_conversation(convo_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses a single conversation dictionary from ChatGPT's export.
    """
    ordered_messages = []
    current_node_id = convo_data.get("current_node")
    mapping = convo_data.get("mapping", {})

    while current_node_id:
        node = mapping.get(current_node_id)
        if not node:
            break

        message_data = node.get("message")
        if (
            message_data
            and message_data.get("content")
            and message_data["author"]["role"] != "system"
        ):
            content_parts = []
            for part in message_data["content"].get("parts", []):
                if isinstance(part, str):
                    content_parts.append(part)
                elif isinstance(part, dict) and 'text' in part:
                    content_parts.append(part['text'])
            content = "".join(content_parts)

            if content:
                role = message_data["author"]["role"]
                if role == "assistant":
                    role = "model"
                ordered_messages.append({"role": role, "parts": [{"text": content}]})

        current_node_id = node.get("parent")

    ordered_messages.reverse()

    return {
        "title": convo_data.get("title", "Untitled Conversation"),
        "history": ordered_messages,
    }

def process_chatgpt_export(input_dir: str) -> List[Dict[str, Any]]:
    """
    Finds and processes the conversations.json file from the export directory.
    """
    json_path = os.path.join(input_dir, "conversations.json")

    if not os.path.exists(json_path):
        print(f"❌ Error: 'conversations.json' not found in '{input_dir}'")
        print("Please provide the path to the root of the unzipped ChatGPT export.")
        return []

    print(f"✅ Found 'conversations.json' at: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        all_conversations_data = json.load(f)

    print(f"Parsing {len(all_conversations_data)} conversations...")

    processed_conversations = [
        parse_conversation(convo)
        for convo in all_conversations_data
        if convo.get("mapping")
    ]

    print(f"✅ Parsing complete.")
    print(f"migrated_conversations={len(processed_conversations)}")
    return processed_conversations

def save_conversations_by_project(conversations: List[Dict[str, Any]], output_dir: str, summarize: bool):
    """Saves all conversations to a structured JSON file."""
    print(f"Summarize flag: {summarize}")
    projects = {}
    for convo in conversations:
        project_name = get_project_name(convo['title'])
        if project_name not in projects:
            projects[project_name] = []
        projects[project_name].append(convo)

    for project_name, convos in projects.items():
        project_dir = os.path.join(output_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)

        if summarize:
            print("Summarizing conversations...")
            for convo in convos:
                convo['summary'] = generate_summary(convo)

        output_path = os.path.join(project_dir, "conversations.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(convos, f, indent=2)
        print(f"💾 Successfully saved {len(convos)} conversations for project '{project_name}' to: {output_path}")

def main():
    """Main function to run the script from the command line."""
    parser = argparse.ArgumentParser(
        description="Process a ChatGPT data export folder into Gemini API format."
    )
    parser.add_argument(
        "input_dir", help="Path to the unzipped ChatGPT export directory."
    )
    parser.add_argument(
        "--output_dir",
        default="gemini_projects",
        help="Path to save the output projects. (e.g., my_projects)",
    )
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Generate a summary for each conversation.",
    )
    args = parser.parse_args()

    processed_data = process_chatgpt_export(args.input_dir)

    if not processed_data:
        print("No conversations were processed. Exiting.")
        return

    save_conversations_by_project(processed_data, args.output_dir, args.summarize)

if __name__ == "__main__":
    main()