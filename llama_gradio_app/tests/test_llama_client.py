"""Tests for the llama_client module."""

import unittest
from unittest.mock import patch, MagicMock

from src.llama_client import generate_response


class TestLlamaClient(unittest.TestCase):
    """Test cases for the llama_client module."""

    def test_empty_message(self):
        """Test handling of empty messages."""
        client = MagicMock()
        result = generate_response(client, "", [], 0.7, 256)
        self.assertEqual(result, "Please enter a message to generate a response.")

    @patch("llama_api_client.LlamaAPIClient")
    def test_message_formatting(self, mock_client):
        """Test message formatting from chat history."""
        # Create a mock client and response
        client = MagicMock()
        mock_response = MagicMock()
        client.chat.completions.create.return_value = mock_response

        # Configure the mock to return a specific response
        mock_response.completion_message.content = "Test response"

        # Test with some history
        history = [("Hello", "Hi there"), ("How are you?", "I'm doing well!")]
        message = "What's your name?"

        with patch.object(
            mock_response.completion_message, "content", "My name is Llama"
        ):
            result = generate_response(client, message, history, 0.7, 256)

            # Verify the right messages were sent to the API
            _, kwargs = client.chat.completions.create.call_args
            messages = kwargs.get("messages", [])

            # Check if history was formatted correctly
            self.assertEqual(len(messages), 5)  # 2 pairs from history + current message
            self.assertEqual(messages[0]["role"], "user")
            self.assertEqual(messages[0]["content"], "Hello")
            self.assertEqual(messages[1]["role"], "assistant")
            self.assertEqual(messages[1]["content"], "Hi there")

            # Check current message
            self.assertEqual(messages[4]["role"], "user")
            self.assertEqual(messages[4]["content"], "What's your name?")


if __name__ == "__main__":
    unittest.main()
