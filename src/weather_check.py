import asyncio
import os


from random import randint

from agent_framework import Agent, tool

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

from agent_framework._tools import tool, Field
from typing import Annotated

@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")]
) -> str:
     conditions = ["sunny", "cloudy", "rainy", "stormy"]
     return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


async def main() -> None:
 
    client = FoundryChatClient(
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model="gpt-5-mini",
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="HelloAgent",
        instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
        tools=[get_weather],
    )
  
    async for chunk in agent.run("Tell me the chennai weather now", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()
  

if __name__ == "__main__":
    asyncio.run(main())

