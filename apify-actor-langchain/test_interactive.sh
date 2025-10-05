#!/bin/bash
# Test script for interactive prompting

cd "$(dirname "$0")"
source venv/bin/activate

echo "🧪 Testing Interactive Prompt Feature"
echo ""
echo "The actor will now prompt for a query..."
echo ""

python -m src
