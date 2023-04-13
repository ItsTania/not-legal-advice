import os

import openai
import pinecone
import streamlit as st
from pydantic import BaseSettings


# Load environment variables
class Settings(BaseSettings):
    OPENAI_API_KEY: str = "OPENAI_API_KEY"
    PINECONE_API_KEY: str = "PINECONE_API_KEY"
    PINECONE_ENVIRONMENT: str = "PINECONE_ENVIRONMENT"
    INDEX_NAME: str = "INDEX_NAME"

    class Config:
        env_file = ".env"


settings = Settings()

# Initialize OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

# Initialize Pinecone API key
pinecone.init(
    api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT
)

index = pinecone.Index(settings.INDEX_NAME)

# Streamlit app
col1, col2, col3 = st.columns(3)
with col1:
    st.write(" ")
with col2:
    st.image("logo.png", width=40)

with col3:
    st.write(" ")

st.title("Not Legal Advice: An AI tool to help you understand Australian law")


st.write(
    """
    Reading through law documents is not fun. This tool uses AI to search through law documents to find what you need to know, and which documents it used to find the answer. Enter a question below and click "Search" to get started.
    """
)

prompt = st.text_input(
    "AI Prompt", "Eg. how many times can my rental agent enter my property?"
)

if st.button("Search"):
    st.write("Searching...")
    response = index.search(
        query=prompt, query_by="prompt", filter_by="document_type:law", num_results=5
    )
    st.write("Done!")
    st.write("Results:")
    for result in response:
        st.write(result)
