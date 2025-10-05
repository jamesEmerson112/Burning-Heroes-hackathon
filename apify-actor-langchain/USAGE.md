# Apify Actor LangGraph - Usage Guide

## Running the Actor

The actor **always prompts** for your query on every run, with smart reuse capability.

### Basic Usage

```bash
cd apify-actor-langchain
source venv/bin/activate
python -m src
```

### Interactive Prompt Behavior

**First Run (No Previous Query):**
```
🤖 Enter your query:

Examples:
  • What is 100 + 250 + 375?
  • Get the total likes and comments for latest 10 posts on @openai Instagram

Your query: _
```

**Subsequent Runs (With Previous Query):**
```
🤖 Enter your query:

Previous query: Calculate 25 times 4
(Press Enter to reuse, or type a new query)

Examples:
  • What is 100 + 250 + 375?
  • Get the total likes and comments for latest 10 posts on @openai Instagram

Your query: _
```

- **Press Enter** → Reuses previous query
- **Type new query** → Runs with new query and saves it

## Output

The agent response is displayed clearly in the terminal:

```
============================================================
📝 AGENT RESPONSE
============================================================

Query: Calculate 25 times 4

Response:
25 times 4 is 100.

============================================================
```

Additionally, results are saved to:
- **Text response**: `storage/key_value_stores/default/response.txt`
- **Structured data**: `storage/datasets/default/000000001.json`
- **Latest query**: `storage/key_value_stores/default/INPUT`

## Available Tools

The agent has access to two tools:

1. **Calculator** - Sums a list of numbers
   - Example: "What is 100 + 250 + 375?"

2. **Instagram Scraper** - Fetches Instagram profile posts
   - Example: "Get the total likes for latest 10 posts on @nasa Instagram"
   - Note: Requires valid APIFY_API_TOKEN in `.env`

## Configuration

**Model**: gpt-4.1-2025-04-14 (default)
**Debug Mode**: Enabled by default (shows tool calls and reasoning)

To change settings, edit the `actor_input` dictionary in `src/main.py`.
