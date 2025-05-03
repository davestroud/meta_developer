"""Llama API client module."""

import os
from llama_api_client import LlamaAPIClient


def initialize_client():
    """Initialize and return a Llama API client.

    Returns:
        LlamaAPIClient: Configured API client instance
    """
    api_key = os.getenv("LLAMA_API_KEY")
    api_url = os.getenv("API_URL", "https://api.llama.com/v1/")

    if not api_key or api_key == "your_llama_api_key_here":
        raise ValueError("Please set your Llama API key in the .env file.")

    return LlamaAPIClient(
        api_key=api_key,
        base_url=api_url,
    )


def generate_response(
    client,
    message,
    history,
    temperature=0.7,
    max_tokens=256,
    model_id="Llama-4-Maverick-17B-128E-Instruct-FP8",
):
    """Generate a response from Llama using the Meta Developer API.

    Args:
        client (LlamaAPIClient): Initialized Llama API client
        message (str): User input text
        history (list): Conversation history
        temperature (float): Controls randomness (0.0 to 1.0)
        max_tokens (int): Maximum tokens to generate
        model_id (str): Model identifier

    Returns:
        str: Generated text response
    """
    if not message.strip():
        return "Please enter a message to generate a response."

    # Format messages for the API
    messages = []

    # Convert Gradio's chatbot format to the API's format
    if history:
        for item in history:
            if isinstance(item, tuple) and len(item) == 2:
                user_msg, bot_msg = item
                if user_msg:
                    messages.append({"role": "user", "content": user_msg})
                if bot_msg:
                    messages.append({"role": "assistant", "content": bot_msg})

    # Add the current message
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=temperature,
        )

        # Extract the completion message content based on the structure
        if hasattr(response, "completion_message"):
            if hasattr(response.completion_message, "content"):
                # Check if content is a MessageTextContentItem
                if hasattr(response.completion_message.content, "text"):
                    return response.completion_message.content.text
                # Or if it's a direct string
                elif isinstance(response.completion_message.content, str):
                    return response.completion_message.content

        # Return full response as last resort
        return str(response)

    except Exception as e:
        return f"Error: {str(e)}"
