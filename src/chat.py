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

    #session creation 

    agent_session = agent.create_session()
    
    response = await agent.run("Hello am bharathi from chennai, how you doing?", session=agent_session)
    print(f"Agent : {response}\n")

    response = await agent.run("Hey do you know where I live?", session = agent_session)
    print(f"Agent :{response}")

    async for word in agent.run("Do you know my name", session = agent_session, stream = True):
        if word.text:
            print(word.text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())