import json
import os
import argparse
from typing import List, Dict, Any

def parse_conversation(convo_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses a single conversation dictionary from ChatGPT's export.

    The messages are stored in a graph-like structure. This function
    traverses it backwards from the last message to reconstruct the
    chronological order.

    Args:
        convo_data: The dictionary for a single conversation.

    Returns:
        A dictionary containing the conversation's title and an ordered
        list of messages in Gemini API format.
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

    Args:
        input_dir: The path to the unzipped ChatGPT export folder.

    Returns:
        A list of all parsed conversations.
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

def save_as_json(conversations: List[Dict[str, Any]], output_path: str):
    """Saves all conversations to a structured JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=2)
    print(f"💾 Successfully saved structured JSON output to: {output_path}")

def main():
    """Main function to run the script from the command line."""
    parser = argparse.ArgumentParser(
        description="Process a ChatGPT data export folder into Gemini API format."
    )
    parser.add_argument(
        "input_dir", help="Path to the unzipped ChatGPT export directory."
    )
    parser.add_argument(
        "--output_file",
        default="gemini_archive.json",
        help="Path to save the output as a structured .json file. (e.g., output.json)",
    )
    args = parser.parse_args()

    processed_data = process_chatgpt_export(args.input_dir)

    if not processed_data:
        print("No conversations were processed. Exiting.")
        return

    save_as_json(processed_data, args.output_file)

if __name__ == "__main__":
    main()
