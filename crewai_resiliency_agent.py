from crewai import Agent, Task, Crew

# Define an agent
resiliency_advisor = Agent(
    role="Researcher",
    goal="Find and summarize AWS resiliency best practices",
    backstory="An expert cloud architect who keeps up with AWS trends."
)

# Define a task
task = Task(
    description="Search for the latest AWS resiliency best practices and summarize them.",
    agent=researcher,
    expected_output="A concise summary of AWS resiliency best practices."
)

# Create a crew
crew = Crew(
    agents=[researcher],
    tasks=[task]
)

# Run the crew
result = crew.kickoff()
print(result)
