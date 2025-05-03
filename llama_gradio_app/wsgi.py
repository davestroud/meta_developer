"""WSGI entry point for the Llama Gradio App."""

import os
from dotenv import load_dotenv

# Load environment variables at startup
load_dotenv()

# Import the application
from src.main import create_app

# Create the application instance
app = create_app()

# This is used by gunicorn
application = app.app

if __name__ == "__main__":
    application.run()
