#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="llama_gradio_app",
    version="0.1.0",
    description="A Gradio app for interacting with Llama models",
    author="David Stroud",
    author_email="david@davidstroud.me",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "gradio>=5.29.0,<6.0.0",
        "requests>=2.32.3,<3.0.0",
        "python-dotenv>=1.1.0,<2.0.0",
        "llama-api-client>=0.1.0,<0.2.0",
    ],
    entry_points={
        "console_scripts": [
            "llama-app=llama_gradio_app.app:main",
        ],
    },
)
