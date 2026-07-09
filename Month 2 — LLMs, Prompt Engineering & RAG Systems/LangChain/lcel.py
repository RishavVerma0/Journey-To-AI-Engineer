# I am trying to understand LCEL using this file 

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_cerebras import ChatCerebras
from dotenv import load_dotenv
import os 

load_dotenv()

api_key = os.getenv("API_KEY")

# Add validation to ensure the key exists
if not api_key:
    raise ValueError("API_KEY environment variable is not set")

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in one sentence for a {audience}."
)

llm = ChatCerebras(
    model="gpt-oss-120b",
    temperature=0.3,
    api_key=api_key, # type: ignore
)
parser = StrOutputParser()

chain = prompt | llm | parser 

inputs =[
    {"topic": "gravity", "audience": "5-year-old"},
    {"topic": "gravity", "audience": "physice PhD student"},
    {"topic": "blockchain", "audience": "small bussiness owner"}
]

for i in inputs:
    print(i, "->", chain.invoke(i),"\n")