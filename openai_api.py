from openai import OpenAI
from dotenv import load_dotenv
import os

# Loading the OPEN AI API KEY
env_path=r'C:\openai_api.env'
load_dotenv(env_path)

# Initialize OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Sending input to the OpenAI client using LLM model gpt-4o-mini

response = client.responses.create(
    model="gpt-4o-mini",
    input="Weather in California."
)

print(response.output_text)
