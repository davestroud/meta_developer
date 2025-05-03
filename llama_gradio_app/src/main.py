"""Main entry point for the Llama Gradio App."""

import os
import argparse
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
    parser.add_argument(
        "--share-duration",
        type=int,
        default=259200,
        help="Duration in seconds for the share link to be valid (default: 72 hours)",
    )
    return parser.parse_args()


def main():
    """Initialize and launch the Gradio interface."""
    global client

    # Parse command line arguments
    args = parse_args()

    # Determine share status (--no-share takes precedence over --share)
    share = (
        True if args.share and not args.no_share else False if args.no_share else True
    )

    # Load environment variables
    load_dotenv()

    # Initialize Llama client
    client = initialize_client()

    # Create and launch Gradio interface
    demo = create_interface(respond)

    # Launch with sharing enabled
    # When share=True, a public, shareable link will be generated
    demo.launch(
        share=share,  # Enable/disable based on command line args
        server_name="0.0.0.0",  # Make server accessible on local network
        server_port=args.port,  # Port from command line args
        show_error=True,  # Show detailed error messages
        favicon_path=None,  # Optional: path to favicon icon
        share_server_duration=args.share_duration,  # Link duration from command line args
    )


if __name__ == "__main__":
    main()
