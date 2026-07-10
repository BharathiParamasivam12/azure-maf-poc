import asyncio
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Foundry client
project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
model = os.getenv("FOUNDRY_MODEL") or "gpt-5-mini"

if not project_endpoint:
    raise ValueError("FOUNDRY_PROJECT_ENDPOINT is required. Set it in your environment or .env file.")

client = FoundryChatClient(
    project_endpoint=project_endpoint,
    model=model,
    credential=AzureCliCredential(),
)

# Create agents
writer = Agent(
    name="WriterAgent",
    instructions="Write a short poem (4 lines max) about the given topic.",
    client=client,
)

reviewer = Agent(
    name="ReviewerAgent",
    instructions="Review the given poem in one sentence. Is it good?",
    client=client,
)


async def run_poem_workflow(topic: str) -> str:
    poem = (await writer.run(f"Write a short poem about: {topic}")).text
    review = (
        await reviewer.run(
            f"Review the following poem in one sentence. Is it good?\n\n{poem}"
        )
    ).text
    return f"Poem:\n{poem}\n\nReview:\n{review}"


async def main() -> None:
    result = await run_poem_workflow("a cat learning to code")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
