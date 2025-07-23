from langchain_google_genai import GoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
import os
from dotenv import load_dotenv
from .prompt_templates import generate_story_prompt
load_dotenv()


def generate_story(question: str):
    """Generates a story using a language model and returns the response."""
    llm = GoogleGenerativeAI(model="gemini-2.5-pro", 
                             api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = generate_story_prompt()

    chain = prompt | llm | StrOutputParser()

    response_llm = chain.invoke({"question": question})
    return response_llm
