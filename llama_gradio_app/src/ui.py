"""Gradio UI module for Llama chat interface."""

import gradio as gr

MODEL_ID = "Llama-4-Maverick-17B-128E-Instruct-FP8"


def create_interface(respond_callback):
    """Create and configure the Gradio interface.

    Args:
        respond_callback (callable): Callback function for handling responses

    Returns:
        gr.Blocks: Configured Gradio interface
    """
    with gr.Blocks(title="Llama Chat App") as demo:
        gr.Markdown("# Llama AI Chat")
        gr.Markdown(f"Have a conversation with {MODEL_ID}")

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    height=400,
                    show_copy_button=True,
                    label="Conversation",
                )

                msg = gr.Textbox(
                    placeholder="Type your message here...",
                    label="Your message",
                    show_label=False,
                    container=False,
                )

                with gr.Row():
                    submit_btn = gr.Button("Send", variant="primary")
                    clear_btn = gr.Button("Clear")

            with gr.Column(scale=1):
                temperature = gr.Slider(
                    minimum=0.1, maximum=1.0, value=0.7, step=0.1, label="Temperature"
                )

                max_tokens = gr.Slider(
                    minimum=50, maximum=1000, value=256, step=50, label="Max Tokens"
                )

        # Use the same respond function for both button click and Enter key
        submit_btn.click(
            fn=respond_callback,
            inputs=[msg, chatbot, temperature, max_tokens],
            outputs=[msg, chatbot],
        )

        msg.submit(
            fn=respond_callback,
            inputs=[msg, chatbot, temperature, max_tokens],
            outputs=[msg, chatbot],
        )

        clear_btn.click(lambda: ("", []), None, [msg, chatbot])

        # Default examples
        gr.Examples(
            examples=[
                "Tell me a short story about a robot learning to paint.",
                "Explain quantum computing in simple terms.",
                "Write a haiku about the changing seasons.",
            ],
            inputs=msg,
        )

    return demo
