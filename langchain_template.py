from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Translate this from {input_language} to {output_language}: {text}"
)

prompt = template.format(
    input_language="English",
    output_language="Spanish",
    text="Hello, how are you?"
)

print(prompt)
# Translate this from English to Spanish: Hello, how are you?

# This generates a structured chat message list, ready for an LLM.

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "{user_input}")
])

filled = prompt.invoke({
    "name": "Rajasekar",
    "user_input": "What is LangChain?"
})

print(filled)
