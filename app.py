import os

import openai
import pinecone
import streamlit as st
from pydantic import BaseSettings

# from src.download_docs_utils import *
# from src.preprocess_docs_utils import *
# from src.vector_database_utils import *
# from src.gpt_utils import *

# Load environment variables
class Settings(BaseSettings):
    OPENAI_API_KEY: str = "OPENAI_API_KEY"
    PINECONE_API_KEY: str = "PINECONE_API_KEY"
    PINECONE_ENVIRONMENT: str = "PINECONE_ENVIRONMENT"
    INDEX_NAME: str = "INDEX_NAME"
    EMBED_MODEL: str = "EMBED_MODEL"
    QUERY_MODEL: str = "QUERY_MODEL"

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
st.title("Not Legal Advice: An AI tool to help you understand Australian law")

st.write(
    """
    Reading through law documents is not fun. This tool uses AI to search through law documents to find what you need to know, and which documents it used to find the answer. Enter a question below and click "Search" to get started.
    """
)

prompt = st.text_input(
    "", "Eg. how many times can my rental agent enter my property?"
)

# Slider to control number of documents to return
num_docs = st.slider("Number of documents to return", 1, 10, 5)

if st.button("Search"):
    with st.spinner(f"Searching through the {settings.INDEX_NAME} database..."):
        # Embed the prompt
        embedded_prompt = openai.Embedding.create(
            input=[prompt],
            engine=settings.EMBED_MODEL
        )

        # Search the index
        res = index.query(embedded_prompt['data'][0]['embedding'], top_k=num_docs, include_metadata=True)

        # Get the tests
        contexts = [item['metadata']['text'] for item in res['matches']]
        augmented_query = "\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+prompt

    with st.spinner(f"Asking {settings.QUERY_MODEL} for their interpretation..."):
        # Define the primer to make it less likely to hallucinate nonsense
        primer = f"""You are Q&A bot. A highly intelligent system that answers
        user questions based on the information provided by the user above
        each question. If the information can not be found in the information
        provided by the user you truthfully say "I don't know".
        """

        # Send the augmented query to GPT-3
        response = openai.ChatCompletion.create(
            model=settings.QUERY_MODEL,
            messages=[
                {"role": "system", "content": primer},
                {"role": "user", "content": augmented_query}
            ]
        )
    st.write("Done! Here are the results:")
    st.markdown(response['choices'][0]['message']['content'])

    st.write("Here are the documents that were used to find the answer:")
    for i, context in enumerate(contexts):
        st.write(f"Document {i+1}:")
        st.write(context)
