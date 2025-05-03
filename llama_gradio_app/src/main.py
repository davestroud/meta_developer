"""Main entry point for the Llama Gradio App."""

import os
import argparse
from dotenv import load_dotenv

from .llama_client import initialize_client, generate_response
from .ui import create_interface, MODEL_ID

# Global client for API calls
client = None


def respond(message, chat_history, temp, tokens):
    """Callback function to handle user messages and generate responses.

    Args:
        message (str): User message
        chat_history (list): Chat history in messages format
        temp (float): Temperature parameter
        tokens (int): Maximum tokens to generate

    Returns:
        tuple: Empty message and updated chat history
    """
    # Convert messages format to format expected by generate_response if needed
    history_tuples = []
    if chat_history:
        for msg in chat_history:
            if msg.get("role") == "user" and len(history_tuples) > 0:
                # If we have a user message, add it to the last assistant message
                history_tuples[-1] = (history_tuples[-1][0], msg.get("content", ""))
            elif msg.get("role") == "assistant" and len(history_tuples) > 0:
                # If we have an assistant message, add it to the last user message
                history_tuples[-1] = (history_tuples[-1][0], msg.get("content", ""))
            elif msg.get("role") == "user":
                # Start a new message pair
                history_tuples.append((msg.get("content", ""), ""))

    # Get response from Llama
    bot_message = generate_response(
        client, message, history_tuples, temp, tokens, MODEL_ID
    )

    # Add messages in the format expected by the updated Chatbot component
    chat_history.append({"role": "user", "content": message})
    chat_history.append({"role": "assistant", "content": bot_message})

    return "", chat_history


def parse_args():
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Llama Gradio App")
    parser.add_argument(
        "--share",
        action="store_true",
        help="Enable sharing of the app with a public URL",
    )
    parser.add_argument(
        "--no-share",
        action="store_true",
        help="Disable sharing of the app (overrides --share)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port to run the app on (default: 7860)",
    )
    # Note: share_duration parameter removed as it's not supported in the current Gradio version
    return parser.parse_args()


def create_app():
    """Initialize and create the Gradio application.

    Returns:
        gr.Blocks: The configured Gradio application
    """
    global client

    # Initialize the client if it doesn't exist yet
    if client is None:
        # Load environment variables
        load_dotenv()
        # Initialize Llama client
        client = initialize_client()

    # Create Gradio interface
    demo = create_interface(respond)

    return demo


def main():
    """Initialize and launch the Gradio interface for CLI usage."""
    # Parse command line arguments
    args = parse_args()

    # Determine share status (--no-share takes precedence over --share)
    share = (
        True if args.share and not args.no_share else False if args.no_share else True
    )

    # Create application
    demo = create_app()

    # Launch with sharing enabled
    # When share=True, a public, shareable link will be generated
    demo.launch(
        share=share,  # Enable/disable based on command line args
        server_name="0.0.0.0",  # Make server accessible on local network
        server_port=args.port,  # Port from command line args
        show_error=True,  # Show detailed error messages
        # Simplified parameters for compatibility with Gradio 5.29.0
    )


if __name__ == "__main__":
    main()
