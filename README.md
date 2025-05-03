# Llama Gradio App

A simple Gradio application for interacting with the Llama AI model using the Meta Developer API.

## Features
- Chat interface using Gradio
- Integration with the Llama-4-Maverick-17B-128E-Instruct-FP8 model
- Temperature and token length control
- Modular architecture for easy maintenance
- Shareable public URL for easy demo sharing

## Project Structure
```
llama_gradio_app/
├── src/                    # Source code
│   ├── __init__.py
│   ├── llama_client.py     # Llama API client functionality
│   ├── ui.py               # Gradio UI components
│   └── main.py             # Main application logic
├── tests/                  # Test modules
│   ├── __init__.py
│   └── test_llama_client.py
├── app.py                  # Entry point
└── pyproject.toml          # Poetry configuration
```

## Setup

### With Poetry (recommended)
1. Install dependencies: `poetry install`
2. Create a `.env` file with your Llama API key: `LLAMA_API_KEY=your_api_key_here`
3. Run the app: `poetry run python app.py`
4. Access the app locally at: http://localhost:7860
5. A public shareable link will be generated automatically (looks like: https://xxxx.gradio.live)

### With pip
1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your Llama API key: `LLAMA_API_KEY=your_api_key_here`
3. Run the app: `python app.py`
4. Access the app locally at: http://localhost:7860
5. A public shareable link will be generated automatically (looks like: https://xxxx.gradio.live)

## Sharing Options

By default, shared links are active for 72 hours. You can control sharing behavior using command-line arguments:

```bash
# Run with sharing enabled (default)
python app.py

# Explicitly enable sharing
python app.py --share

# Disable sharing
python app.py --no-share

# Change the port
python app.py --port 8000

# Change the sharing duration (in seconds)
python app.py --share-duration 43200  # 12 hours
```

You can also modify the sharing parameters in the code by adjusting the `launch()` parameters in `src/main.py`:

For permanent hosting, consider deploying to:
- [Hugging Face Spaces](https://huggingface.co/spaces) (recommended)
- Your own server with Docker or a web server

## Sharing FAQ

### How does Gradio sharing work?
When you enable sharing, Gradio creates a tunnel to your locally running app and generates a public URL that anyone can access. The computation still happens on your local machine.

### Is my API key secure when sharing?
Yes, your API key remains on your local machine. The Gradio sharing feature only creates a tunnel for web traffic, not direct access to your files or environment variables.

### Can I control who can access my shared app?
Currently, basic sharing doesn't support authentication. For access control, consider:
- Deploying to Hugging Face Spaces with privacy settings
- Setting up authentication through a custom web server

### What happens when I close my laptop or terminate the script?
The shared link will stop working as soon as your local server stops running. The app needs to be running continuously for the link to work.

### How can I make my app permanently available?
For permanent hosting, deploy to:
- Hugging Face Spaces (free, persistent hosting with GitHub integration)
- Your own server (using Docker, nginx, etc.)
- A cloud provider (AWS, Google Cloud, etc.)

## Development
- Run tests: `python -m unittest discover -s tests`
- Format code: Use Black or another PEP 8 compliant formatter

## License
MIT 