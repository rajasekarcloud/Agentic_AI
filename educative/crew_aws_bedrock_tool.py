from crewai import Agent, Crew, Task, LLM, Process
import boto3
from crewai_tools import tool
import os 

os.environ["AWS_ACCESS_KEY_ID"] = "xxx" # Access key
os.environ["AWS_SECRET_ACCESS_KEY"] = "xxx" # Secret access key
os.environ["AWS_REGION_NAME"] = "us-east-1"

model_arn = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"
model_id = model_id = model_arn.split('/')[-1]

# Define the tool
@tool("LaptopTools")
def LaptopTools(question: str) -> str:
    """This expert has access to all details about the laptops we have in our inventory"""
    query = question
    print("im running")
    client = boto3.client('bedrock-agent-runtime', region_name='us-east-1', aws_access_key_id='xxx',
                           aws_secret_access_key='xxx')
    # Call the retrieve_and_generate API
    response = client.retrieve_and_generate(
        input={'text': query},
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': 'CBSZBRUUN6',
                'modelArn': model_arn
            }
        },
    )

    # Extract and return the output text
    output_data = response.get('output', {}).get('text', '')
    return output_data

#define Agents
customer_support = Agent(
  role="customer support agent",
  goal="Determine the optimal laptop specifications tailored to the customer's specific needs and usage patterns",
  backstory="You are an experienced customer support agent with a knack for finding the perfect laptop according to the customer's specific needs and usage patterns. Your expertise ensures that all customer requirements are met efficiently.",
  verbose = True,
  llm=LLM(model=f"bedrock/{model_id}")
)

inventory_specialist = Agent (
    role="store inventory specialist",
    goal="Get laptop specifications as an input and then try to find the closest match you find by asking LaptopTools.",
    backstory="You work in my store and help customers to find the laptop available in our store using the given specifications. You always ask LaptopTools before giving a response to make sure the laptop you are suggestion is available",
    tools=[LaptopTools],
    verbose=True,
    llm=LLM(model=f"bedrock/{model_id}")
)


# Define the tasks
customer_support_task = Task(
    description="find the specifications for a laptop that fulfills the customer's requirements in the query {task}",
    expected_output="answer to the query",
    agent=customer_support
)

inventory_specialist_task = Task(
    description="Review the specifications provided by the Customer support agent and then use the tool LaptopTools to find the name and price of the laptop that best matches these requirements.",
    expected_output="A list of the laptops that match customer specifications along with the laptops details like its name and price",
    agent=inventory_specialist
)


# Define the crew
crew = Crew(
    agents=[customer_support, inventory_specialist],
    tasks=[customer_support_task, inventory_specialist_task],
    process=Process.sequential,
    verbose=True
)

inputs = {
    'task': 'I want a laptop that will be used for playing heavy gaming'
}

# Kickoff the project with the specified topic
result = crew.kickoff(inputs=inputs)
