"""Main entry point for the Llama Gradio App."""

import os
from dotenv import load_dotenv

from .llama_client import initialize_client, generate_response
from .ui import create_interface, MODEL_ID


def respond(message, chat_history, temp, tokens):
    """Callback function to handle user messages and generate responses.

    Args:
        message (str): User message
        chat_history (list): Chat history
        temp (float): Temperature parameter
        tokens (int): Maximum tokens to generate

    Returns:
        tuple: Empty message and updated chat history
    """
    bot_message = generate_response(
        client, message, chat_history, temp, tokens, MODEL_ID
    )
    chat_history.append((message, bot_message))
    return "", chat_history


def main():
    """Initialize and launch the Gradio interface."""
    global client

    # Load environment variables
    load_dotenv()

    # Initialize Llama client
    client = initialize_client()

    # Create and launch Gradio interface
    demo = create_interface(respond)
    demo.launch()


if __name__ == "__main__":
    main()
