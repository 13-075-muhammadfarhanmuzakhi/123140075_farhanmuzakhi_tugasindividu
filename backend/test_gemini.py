#!/usr/bin/env python
"""Test script to verify Gemini API and list available models"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}..." if api_key else "No API key found")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

try:
    genai.configure(api_key=api_key)
    print("✓ API configured successfully")
    
    # List available models
    print("\n📋 Available models:")
    for model in genai.list_models():
        print(f"  - {model.name}")
    
    # Try to use the first available model
    print("\n🧪 Testing API with a simple request...")
    models = list(genai.list_models())
    if models:
        model_name = models[0].name
        print(f"Using model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, write one sentence about product reviews.")
        print(f"✓ Response: {response.text}")
    else:
        print("ERROR: No models available")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
