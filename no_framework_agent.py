# Define your tools
def add_numbers(x, y):
    return x + y

def search_web(query):
    return f"Fake search results for: {query}"

# Define the system prompt
# This tells the LLM how to behave like an agent.
SYSTEM_PROMPT = """
You are an agent. You can think, decide, and call tools.

TOOLS:
1. add_numbers(x, y)
2. search_web(query)

When you want to use a tool, respond ONLY in this JSON format:

{
  "tool": "<tool_name>",
  "args": { ... }
}

When you want to give the final answer, respond:

{
  "final": "<your answer>"
}
"""
# This is the same pattern used by ReAct, AutoGPT, CrewAI, LangChain Agents, etc.

# LLM wrapper
from openai import OpenAI
from dotenv import load_dotenv
import os

# Loading the OPEN AI API KEY
env_path=r'C:\Users\rajas\PycharmProjects\Agentic_AI\Crew_AI\openai_api.env'
load_dotenv(env_path)

# Initialize OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_llm(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

# The agent loop (the heart of the system)
import json

TOOLS = {
    "add_numbers": add_numbers,
    "search_web": search_web
}

def run_agent(user_input):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    while True:
        llm_output = call_llm(messages)

        # Try to parse JSON
        try:
            parsed = json.loads(llm_output)
            print("Parsed LLM Output", parsed)
        except:
            return llm_output  # fallback if LLM returns plain text

        # Final answer
        if "final" in parsed:
            return parsed["final"]

        # Tool call {'tool': 'add_numbers', 'args': {'x': 5, 'y': 7}}
        tool_name = parsed["tool"]
        args = parsed["args"]

        result = TOOLS[tool_name](**args)

        # Feed tool result back to LLM
        messages.append({"role": "assistant", "content": llm_output})
        messages.append({"role": "assistant", "content": str(result)})
        print(messages)

# Run the agent
print(run_agent("What is 5 + 7?"))
#Output:
#12



