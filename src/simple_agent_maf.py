import asyncio
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

"""
Hello Agent — Simplest possible agent
"""
load_dotenv()

async def main() -> None:
    # <create_agent>
    client = FoundryChatClient(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model="gpt-5-mini",
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    # </create_agent>

    result = await agent.run("What is the capital of France?")
    print(f"Agent: {result}")
  
    print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run("Tell me a one-sentence fun fact.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()
  

if __name__ == "__main__":
    asyncio.run(main())