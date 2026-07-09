import asyncio
from agent_framework.ollama import OllamaChatClient

async def main():
    agent = OllamaChatClient(
        model="llama3.1"
    ).as_agent(
        name="SimpleAgent",
        instructions="You are a helpful assistant."
    )

    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break

        response = await agent.run(question)
        print(response)

asyncio.run(main())