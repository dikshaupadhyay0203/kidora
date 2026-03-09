from langchain_google_genai import GoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from .prompt_templates import generate_story_prompt
load_dotenv()


def generate_story(question: str):
    """Generates a story using a language model and returns the response."""
    llm = GoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), 
                             api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = generate_story_prompt()

    chain = prompt | llm | StrOutputParser()

    response_llm = chain.invoke({"question": question})
    return response_llm


def generate_long_story(question: str):
    """Generates a longer paragraph-based story for Story Caves."""
    llm = GoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a creative children's storyteller. Write warm, engaging stories for kids aged 6-12 in simple English."
        ),
        (
            "user",
            "Write a longer story about: {question}."
            "\n\nRequirements:"
            "\n- 4 to 6 paragraphs"
            "\n- Each paragraph should be 3 to 5 sentences"
            "\n- Keep it magical, fun, and age-appropriate"
            "\n- Add a meaningful ending or moral"
            "\n- Return only the story text in paragraphs, no bullet points or numbered steps"
        ),
    ])

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": question})
