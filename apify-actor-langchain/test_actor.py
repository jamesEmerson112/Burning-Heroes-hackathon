#!/usr/bin/env python3
"""Simple test script to run the Apify Actor locally."""

import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Set up test input
os.environ['APIFY_INPUT_VALUE'] = json.dumps({
    'query': 'What is 2 + 2? Use the calculator tool.',
    'debug': True
})

# Import and run the main function
from src.main import main

if __name__ == '__main__':
    print("=" * 60)
    print("Testing Apify LangChain Actor with GPT-4.1")
    print("=" * 60)
    print(f"\nOpenAI API Key present: {bool(os.getenv('OPENAI_API_KEY'))}")
    print(f"Apify API Token present: {bool(os.getenv('APIFY_API_TOKEN'))}")
    print("\nRunning actor...")
    print("=" * 60)

    try:
        asyncio.run(main())
        print("\n" + "=" * 60)
        print("✅ Actor completed successfully!")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Error: {e}")
        print("=" * 60)
        raise
