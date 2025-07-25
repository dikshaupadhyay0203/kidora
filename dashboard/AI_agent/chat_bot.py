from langchain_google_genai import GoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

def generate_rhyme(query: str):
    """Generates a rhyme using a language model and returns the response."""
    llm = GoogleGenerativeAI(model="gemini-2.5-pro", 
                             api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a friendly and creative AI that writes short, fun rhymes or poems for kids aged 5 to 10."""),
        ("user", """Write a short rhyme or poem (8 - 12 lines) about the theme: {query}.

Make it simple, playful, and age-appropriate. Use easy vocabulary and fun rhythm. Avoid long or complex sentences.

Make sure the tone is cheerful and suitable for children's understanding."""),
    ])

    chain = prompt | llm | StrOutputParser()

    response_llm = chain.invoke({"query": query})
    return response_llm


def ask_your_buddy(question: str) -> str:
    """
    Function to ask your AI buddy a question and get a response.
    """
    llm = GoogleGenerativeAI(model="gemini-2.5-pro")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI learning buddy and a companion for kids. Be creative and joyful. Make sure your responses are age-appropriate for kids.Try to be more engaging and make him feel like you are a friend"),
        ("human", "{question}"),
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"question": question})

if __name__ == "__main__":
    # Example usage
    query = "A happy cat playing with a ball of yarn"
    rhyme = generate_rhyme(query)
    print("Generated Rhyme:", rhyme)