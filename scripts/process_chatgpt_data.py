import json
import os
import argparse
from typing import List, Dict, Any

# A constant for a nice separator in the text output file.
CONVERSATION_SEPARATOR = "=" * 80

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
        list of messages.
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
            # The content is in a list of parts, join them.
            content_parts = []
            for part in message_data["content"].get("parts", []):
                if isinstance(part, str):
                    content_parts.append(part)
                elif isinstance(part, dict) and 'text' in part:
                    content_parts.append(part['text'])
            content = "".join(content_parts)
            if content:
                ordered_messages.append(
                    {
                        "role": message_data["author"]["role"],
                        "content": content,
                    }
                )
        
        current_node_id = node.get("parent")

    # The messages were added backwards, so reverse the list for chronological order.
    ordered_messages.reverse()
    
    return {
        "title": convo_data.get("title", "Untitled Conversation"),
        "messages": ordered_messages,
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
        if convo.get("mapping") # Ensure the conversation has messages
    ]

    print(f"✅ Parsing complete.")
    print(f"migrated_conversations={len(processed_conversations)}")
    return processed_conversations

def save_as_text(conversations: List[Dict[str, Any]], output_path: str):
    """Saves all conversations to a single human-readable TXT file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, convo in enumerate(conversations):
            f.write(f"{CONVERSATION_SEPARATOR}\n")
            f.write(f"CONVERSATION {i+1}: {convo['title']}\n")
            f.write(f"{CONVERSATION_SEPARATOR}\n\n")

            for message in convo["messages"]:
                # Capitalize role for better readability (user -> User)
                role = message['role'].capitalize()
                f.write(f"{role}:\n{message['content']}\n\n")
            
            f.write("\n")
    print(f"💾 Successfully saved human-readable output to: {output_path}")

def save_as_json(conversations: List[Dict[str, Any]], output_path: str):
    """Saves all conversations to a structured JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(conversations, f, indent=2)
    print(f"💾 Successfully saved structured JSON output to: {output_path}")

def main():
    """Main function to run the script from the command line."""
    parser = argparse.ArgumentParser(
        description="Process a ChatGPT data export folder into consumable formats."
    )
    parser.add_argument(
        "input_dir",
        help="Path to the unzipped ChatGPT export directory."
    )
    parser.add_argument(
        "--txt",
        help="Path to save the output as a human-readable .txt file. (e.g., output.txt)",
        nargs='?', # Makes the argument optional
        const="chatgpt_export.txt", # Default value if --txt is provided without a path
        default=None
    )
    parser.add_argument(
        "--json",
        help="Path to save the output as a structured .json file. (e.g., output.json)",
        nargs='?',
        const="chatgpt_export.json",
        default=None
    )
    args = parser.parse_args()
    
    if not args.txt and not args.json:
        print("⚠️ Warning: No output format specified. Use --txt and/or --json to save the results.")
        # Default to printing a TXT file if no options are given
        args.txt = "chatgpt_export.txt"

    processed_data = process_chatgpt_export(args.input_dir)

    if not processed_data:
        print("No conversations were processed. Exiting.")
        return

    if args.txt:
        save_as_text(processed_data, args.txt)
    
    if args.json:
        save_as_json(processed_data, args.json)

if __name__ == "__main__":
    main()