import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from googletrans import Translator


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))






def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    translator = Translator()
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain.invoke(
        {"input_documents":docs, "question": user_question})
    
    # print(response)
    # st.write("Reply: ", response["output_text"])
    response_text_english = response["output_text"]
    response_text_original_language = translator.translate (response_text_english,
                                                           dest=translator.detect(response_text_english).lang).text
    print(response_text_original_language)
    st.write("Reply: ", response_text_original_language)
    




def main():
    st.set_page_config("Chat PDF")
    def streamlit_login():
    # Hardcoded username and password for demonstration purposes
           
        valid_username = "user123"
        valid_password = "password123"

        st.sidebar.subheader("Login")
        username_input = st.sidebar.text_input("Username:")
        password_input = st.sidebar.text_input("Password:", type="password")

        if st.sidebar.button("Login"):
            # Check if the entered username and password match the valid credentials
            if username_input == valid_username and password_input == valid_password:
                st.sidebar.success(f"{username_input} You have  successfully Logged In! \n please click on X on top right to close")
                st.title(f"Welcome to the chatbot, {username_input}! :technologist:")

                return True, username_input
                
            else:
                st.sidebar.error("Invalid username or password. Please try again.")
                st.stop()
    def streamlit_logout():
        st.sidebar.subheader("Logout")
        if st.sidebar.button("Logout"):
            st.sidebar.warning("Logout successful!")
            return True
        return False
    
    if streamlit_login():
        
    # Code to execute after successful login (e.g., reading PDFs, chatbot logic)
        #print("Welcome to the chatbot!")
        ##st.title(f"Welcome to the chatbot!' ",":technologist: ")

        st.header("Chat with PDF in Any Language you want💁")

        user_question = st.text_input("Ask a Question from the PDF Files")

        if user_question:
            user_input(user_question)

        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")
        
        if streamlit_logout():
            st.error("Logout. Exiting...")
            st.stop()
    else: 
        st.error("Please Login to Continue")


if __name__ == "__main__":
    main()
