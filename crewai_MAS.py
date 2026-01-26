from crewai import Agent, Task, Crew
import os
from utils import get_openai_api_key, get_serper_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

#1- Chef
chef = Agent(
    role="chef",
    goal="Give 5 different receipes using ingredients : {ingredients}",
    backstory="You're  a Chef who has experience on cooking delicious foods"
              "Your expertice lies in recommeding some new foods to the customers"
              "Please generate and give receipe of 5 different foods using this ingredients : {ingredients} "
              "describing stepwise process, time to cook, other ingredients needed and calorie count"
              "Your recipe will be critically analyzed by nutritutionist to recommend food for diabetes patients ",
    verbose=True
)
2# Nutritionist
nutritionist = Agent(
    role="nutritionist",
    goal="Critically analyze the recipe given by chef using these ingredients: {ingredients}",
    backstory="You're a nutritionist and have good knowledge on working with Diabetic patients "
              "There are recipe recommended by chef using these ingredients : {ingredients}. "
              "please critically analyze the recipe and suggest best food out of goven 5 for Diabetic patients"
              "Also give reasons why you dont recommend other 4 receips and choose this one",
    verbose=True
)

cook = Task(
    description=(
        "1. Write receipe of 5 different foods using these ingredients  : {ingredients}.\n"
    ),
    expected_output="5 different receipes using {ingredients}"
                    "Stepwise guide to cook"
                    "List of all additional ingredients required for cooking"
                    "The expected taste of the food",
    agent=chef,
)

recommend = Task(
    description=(
        "1. Read the receipes provided by chef using {ingredients} \n"
        "2. critically analyze all receipes keeping in mind what should suit to diabetic patients.\n"
        "3. Suggest one best food out of all 5 receipes given by chef.\n"
        "4. Prove that other 4 receipes suggested by chef is not good for diabetic patients.\n"
        
    ),
    expected_output="A well-written critical pointwise analysis of all 5 recipes using {ingredients}"
                    "Suggest one receipe to diabetic patients based on your own knowledge and evidence "
                    "Reject all other 4 receipes with knowledge and evidence "
                    "Finally, give the stepwoise receipe of what you selected and a nice message",
    agent=nutritionist,
)

crewaman = Crew(
    agents=[chef,nutritionist],
    tasks=[cook, recommend],
    verbose=2
)

result = crewaman.kickoff(inputs={"ingredients": "spinach"})
