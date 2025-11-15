# config.example.py
# Configuration template for Azure OpenAI API credentials and endpoints
# 
# INSTRUCTIONS:
# 1. Copy this file to config.py
# 2. Fill in your actual Azure OpenAI credentials
# 3. Update deployment names if different
# 4. Never commit config.py to version control!

import os

# Azure OpenAI Configuration
# Main API Key (used for Whisper and GPT-4o)
AZURE_OPENAI_API_KEY = "your-azure-openai-api-key-here"

# Azure OpenAI Endpoints
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_COGNITIVE_ENDPOINT = "https://your-resource-name.cognitiveservices.azure.com/"

# DALL-E 3 Configuration (may use different endpoint and key)
DALLE_API_KEY = os.getenv("DALLE_API_KEY", AZURE_OPENAI_API_KEY)
DALLE_ENDPOINT = os.getenv("DALLE_ENDPOINT", AZURE_OPENAI_ENDPOINT)

# Model Deployment Names
WHISPER_DEPLOYMENT = "whisper"
DALLE_DEPLOYMENT = "dall-e-3"
GPT4O_DEPLOYMENT = "gpt-4o"

# API Versions
WHISPER_API_VERSION = "2024-06-01"
DALLE_API_VERSION = "2024-02-01"
GPT4O_API_VERSION = "2025-01-01-preview"

# Project Paths
AUDIO_DIR = "audio"
OUTPUT_DIR = "output"
CATEGORIES_FILE = "categories.json"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
