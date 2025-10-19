import unittest
import os
import json
from scripts.process_chatgpt_data import parse_conversation, process_chatgpt_export

class TestProcessChatGPTData(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = 'tests/test_data'
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.conversations = [
            {
                "title": "Test Conversation",
                "current_node": "node1",
                "mapping": {
                    "node1": {
                        "id": "node1",
                        "message": {
                            "author": {"role": "user"},
                            "content": {"parts": ["Hello"]}
                        },
                        "parent": "node0"
                    },
                    "node0": {
                        "id": "node0",
                        "message": {
                            "author": {"role": "assistant"},
                            "content": {"parts": ["Hi there!"]}
                        }
                    }
                }
            }
        ]
        with open(f'{self.test_data_dir}/conversations.json', 'w') as f:
            json.dump(self.conversations, f)

    def tearDown(self):
        os.remove(f'{self.test_data_dir}/conversations.json')
        os.rmdir(self.test_data_dir)

    def test_parse_conversation(self):
        convo_data = {
            "title": "Test Conversation",
            "current_node": "node1",
            "mapping": {
                "node1": {
                    "id": "node1",
                    "message": {
                        "author": {"role": "user"},
                        "content": {"parts": ["Hello"]}
                    },
                    "parent": "node0"
                },
                "node0": {
                    "id": "node0",
                    "message": {
                        "author": {"role": "assistant"},
                        "content": {"parts": ["Hi there!"]}
                    }
                }
            }
        }
        parsed_convo = parse_conversation(convo_data)
        self.assertEqual(parsed_convo['title'], "Test Conversation")
        self.assertEqual(len(parsed_convo['messages']), 2)
        self.assertEqual(parsed_convo['messages'][0]['role'], "assistant")
        self.assertEqual(parsed_convo['messages'][0]['content'], "Hi there!")
        self.assertEqual(parsed_convo['messages'][1]['role'], "user")
        self.assertEqual(parsed_convo['messages'][1]['content'], "Hello")

    def test_process_chatgpt_export(self):
        processed_conversations = process_chatgpt_export(self.test_data_dir)
        self.assertEqual(len(processed_conversations), 1)
        self.assertEqual(processed_conversations[0]['title'], "Test Conversation")

if __name__ == '__main__':
    unittest.main()
