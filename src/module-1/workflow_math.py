import os
import asyncio
from agent_framework import Agent, workflow
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

# step - 1 -Create Foundry client
client = FoundryChatClient(
    project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
    model=os.getenv("FOUNDRY_MODEL") or "gpt-5-mini",
    credential=AzureCliCredential(),
)

# step -2 - Create agents
student = Agent(
    name="StudentAgent",
    instructions="You are a student learning math. Ask questions about math problems.",
    client=client,
)

teacher = Agent(
    name="TeacherAgent",
    instructions="You are a math teacher. Provide clear and concise explanations to the student's questions.",
    client=client,
)

#step - 3 - Define a workflow function
@workflow
async def math_workflow(problem: str) -> str:
    # Student asks a question
    student_question = (await student.run(f"Can you help me with this math problem: {problem}?")).text
    
    # Teacher provides an explanation
    teacher_response = (await teacher.run(f"The student asked: '{student_question}'. Please explain the solution.")).text
    
    return f"Student's Question: {student_question}\nTeacher's Explanation: {teacher_response}"

#step - 4 - Main function to run the workflow
async def main() -> None:
    problem = "What is the square root of 16?"
    result = await math_workflow.run(problem)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
    

