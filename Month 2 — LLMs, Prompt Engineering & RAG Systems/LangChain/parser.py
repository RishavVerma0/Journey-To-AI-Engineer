# I am trying to understand LCEL using this file 

# I am updating my existing code so that i can get the output in a json/pydantic format

from dotenv import load_dotenv
import os

from pydantic import BaseModel, Field

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_cerebras import ChatCerebras

# Load environment variables
load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable is not set")


# Define the schema
class Explanation(BaseModel):
    topic: str = Field(description="The topic explained")
    summary: str = Field(description="One-sentence explanation")
    difficulty: str = Field(description="easy, medium, or hard")


# Create the parser
parser = PydanticOutputParser(pydantic_object=Explanation)


# Create the prompt
prompt = ChatPromptTemplate.from_template(
    """
Explain "{topic}" in exactly one sentence for a {audience}.

Return ONLY valid JSON.
Do NOT wrap the JSON in markdown.
Do NOT include any extra text.
Do NOT use LaTeX or special escape sequences.

{format_instructions}
"""
).partial(
    format_instructions=parser.get_format_instructions()
)


# Initialize the LLM
llm = ChatCerebras(
    model="gpt-oss-120b",
    temperature=0,
    api_key=api_key, # type: ignore
)


# LCEL chain
chain = prompt | llm | JsonOutputParser()


# Inputs
inputs = [
    {"topic": "gravity", "audience": "5-year-old"},
    {"topic": "gravity", "audience": "physics PhD student"},
    {"topic": "blockchain", "audience": "small business owner"},
]


# Invoke
for inp in inputs:
    try:
        result = chain.invoke(inp)

        print(result)
        print("Topic:", result.topic)
        print("Summary:", result.summary)
        print("Difficulty:", result.difficulty)
        print("-" * 50)

    except Exception as e:
        print(f"Error for {inp}:")
        print(e)