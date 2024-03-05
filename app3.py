from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
load_dotenv() #Takes environment variables from .env
import streamlit as st

## Function to load OpenAI model and get responss
##OpenAI.api_key="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"
OPENAI_API_KEY='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'
##OpenAI.api_key=OPENAI_API_KEY
# Q&A Chatbot
#from dotenv import load_dotenv

#load_dotenv()  # take environment variables from .env.


## Function to load OpenAI model and get respones

def get_openai_response(question):
    llm=OpenAI(model_name="gpt-3.5-turbo-instruct",temperature=0.5)
    response=llm(question)
    return response

##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Langchain Application")

input=st.text_input("Input: ",key="input")
response=get_openai_response(input)

submit=st.button("Ask the question")

## If ask button is clicked

if submit:
    st.subheader("The Response is")
    st.write(response)