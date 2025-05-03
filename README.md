# Llama Gradio App

A simple Gradio application for interacting with the Llama AI model using the Meta Developer API.

## Features
- Chat interface using Gradio
- Integration with the Llama-4-Maverick-17B-128E-Instruct-FP8 model
- Temperature and token length control
- Modular architecture for easy maintenance

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

### With pip
1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your Llama API key: `LLAMA_API_KEY=your_api_key_here`
3. Run the app: `python app.py`

## Development
- Run tests: `python -m unittest discover -s tests`
- Format code: Use Black or another PEP 8 compliant formatter

## License
MIT 