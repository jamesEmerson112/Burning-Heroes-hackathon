"""Module defines the main entry point for the Apify Actor.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from apify import Actor
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.models import AgentStructuredOutput
from src.tools import (
    tool_calculator_sum,
    tool_scrape_instagram_profile_posts,
    tool_scrape_yc_company
)
from src.utils import log_state

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


async def main() -> None:
    """Define a main entry point for the Apify Actor.

    This coroutine is executed using `asyncio.run()`, so it must remain an asynchronous function for proper execution.
    Asynchronous execution is required for communication with Apify platform, and it also enhances performance in
    the field of web scraping significantly.

    Raises:
        ValueError: If the input is missing required attributes.
    """
    async with Actor:
        # Charge for Actor start
        await Actor.charge('actor-start')

        # Handle input - Always prompt interactively
        import json

        # Try to load previous query
        previous_query = None
        input_dir = Path(__file__).parent.parent / 'storage' / 'key_value_stores' / 'default'

        # Check for both INPUT and INPUT.json (Apify SDK uses INPUT without extension)
        input_file = input_dir / 'INPUT.json'
        if not input_file.exists():
            input_file = input_dir / 'INPUT'

        if input_file.exists():
            try:
                with open(input_file, 'r') as f:
                    previous_input = json.load(f)
                    previous_query = previous_input.get('query')
            except Exception:
                pass

        # Always show interactive prompt
        print("\n🤖 Enter your query:")
        if previous_query:
            print(f"\nPrevious query: {previous_query}")
            print("(Press Enter to reuse, or type a new query)")

        print("\nExamples:")
        print("  • What is 100 + 250 + 375?")
        print("  • Get the total likes and comments for latest 10 posts on @openai Instagram")
        print()

        query = input("Your query: ").strip()

        # If empty and previous exists, reuse it
        if not query and previous_query:
            query = previous_query
            print(f"✨ Reusing previous query: {query}")
        elif not query:
            msg = 'No query provided!'
            raise ValueError(msg)

        # Use defaults for other settings
        actor_input = {
            'query': query,
            'modelName': 'gpt-4.1-2025-04-14',
            'debug': True
        }

        # Save to INPUT.json
        input_dir.mkdir(parents=True, exist_ok=True)
        with open(input_file, 'w') as f:
            json.dump(actor_input, f, indent=2)

        print(f"\n✅ Using query: {query}")
        print(f"📊 Model: {actor_input['modelName']} | Debug: enabled")
        print(f"💾 Saved to: {input_file}\n")

        query = actor_input.get('query')
        model_name = actor_input.get('modelName', 'gpt-4o-mini')
        if actor_input.get('debug', False):
            Actor.log.setLevel(logging.DEBUG)
        if not query:
            msg = 'Missing "query" attribute in input!'
            raise ValueError(msg)

        llm = ChatOpenAI(model=model_name)

        # Create the ReAct agent graph
        # see https://langchain-ai.github.io/langgraph/reference/prebuilt/?h=react#langgraph.prebuilt.chat_agent_executor.create_react_agent
        tools = [
            tool_calculator_sum,
            tool_scrape_instagram_profile_posts,
            tool_scrape_yc_company
        ]
        graph = create_react_agent(llm, tools, response_format=AgentStructuredOutput)

        inputs: dict = {'messages': [('user', query)]}
        response: AgentStructuredOutput | None = None
        last_message: str | None = None
        async for state in graph.astream(inputs, stream_mode='values'):
            log_state(state)
            if 'structured_response' in state:
                response = state['structured_response']
                last_message = state['messages'][-1].content
                break

        if not response or not last_message:
            Actor.log.error('Failed to get a response from the ReAct agent!')
            await Actor.fail(status_message='Failed to get a response from the ReAct agent!')
            return

        # Print response to console for easy viewing
        print("\n" + "="*60)
        print("📝 AGENT RESPONSE")
        print("="*60)
        print(f"\nQuery: {query}")
        print(f"\nResponse:\n{last_message}")
        print("\n" + "="*60 + "\n")

        # Charge for task completion
        await Actor.charge('task-completed')

        # Push results to the key-value store and dataset
        store = await Actor.open_key_value_store()
        await store.set_value('response.txt', last_message)
        Actor.log.info('Saved the "response.txt" file into the key-value store!')

        await Actor.push_data(
            {
                'response': last_message,
                'structured_response': response.dict() if response else {},
            }
        )
        Actor.log.info('Pushed the into the dataset!')
