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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth


load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


cred = credentials.Certificate('multilingual-chatbot-2b9c5-c26413b00da0.json')

# Check if the app is not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)



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
    



# Existing
def main():
    st.set_page_config("Chat PDF")

    # Create session state
    session_state = st.session_state
    if not hasattr(session_state, "login_status"):
        session_state.login_status = False

    user = None  # Initialize user variable

    st.sidebar.title("Login/Signup:")
    choice = st.sidebar.radio('Choose Action:', ['Login', 'Signup'])
    st.sidebar.write('Hey There! I can see you 👁️ 😋 jk')

    if choice == 'Login':
        

        email_key = "login_email_input"  # Unique key for email input
        email = st.sidebar.text_input('Enter Email Address', key=email_key)

        password_key = "login_password_input"  # Unique key for password input
        password = st.sidebar.text_input('Enter Password', type='password', key=password_key)

        # Button to toggle login status
        login_button_key = "login_button"  # Unique key for login button
        if st.sidebar.button('Login', key=login_button_key):
            session_state.login_status = not session_state.login_status  # Toggle the login status

        if session_state.login_status:
            if st.sidebar.button('Logout'):
                    st.sidebar.write('Logout Successfully')
                    session_state.login_status = False
                    st.toast('Goodbye!', icon='😋')
                    st.stop() 
            try:
                
                user = auth.get_user_by_email(email)
                st.sidebar.write('Login Successfully')
                if session_state.login_status:
                    st.title("Welcome to my Chatbot :technologist: Chat with Multi Lingual PDF")
                    st.header(' This bot will only answer after you submit and process')
                    # Main content area (display only after successful login)
                    user_question_key = "user_question_input"  # Generate a unique key
                    st.subheader("Ask questions like give me summary or any question from the PDF Files")
                    user_question = st.text_input("Ask a Question from the PDF Files", key=user_question_key)
                    if user_question:
                        user_input(user_question)
                    # File upload and processing section
                    
                    pdf_docs_key = "pdf_docs_uploader"  # Generate a unique key
                    pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True, key=pdf_docs_key)

                    submit_process_key = "submit_process_button"  # Generate a unique key
                    if st.button("Submit & Process", key=submit_process_key):
                        with st.spinner("Processing..."):
                            raw_text = get_pdf_text(pdf_docs)
                            text_chunks = get_text_chunks(raw_text)
                            get_vector_store(text_chunks)
                            st.success("Your Document has been Processed!, only ask simple questions now")
                    
                # Stop the app
        
                   

            except:
                st.sidebar.warning('Incorrect Email/Password, Login Failed')
                session_state.login_status = False
                if st.sidebar.button('Logout'):
                    st.snow()
                    st.sidebar.write('Logout Successfully')
                    session_state.login_status = False
                    st.stop()  

           
        else:
             st.info("Please login or signup to access the application.")
        # Set login status to False
    else:
        email_key = "signup_email_input"  # Unique key for signup email input
        email = st.sidebar.text_input('Enter Email', key=email_key)

        password_key = "signup_password_input"  # Unique key for signup password input
        password = st.sidebar.text_input('Enter Password', type='password', key=password_key)

        username_key = "signup_username_input"  # Unique key for signup username input
        username = st.sidebar.text_input('Enter your unique Username', key=username_key)

        if st.sidebar.button('Create New Account'):
            user = auth.create_user(email=email, password=password, uid=username)
            st.sidebar.success('Your Account has been created successfully!')
            st.sidebar.balloons()
            session_state.login_status = True  # Set login status to True after successful signup

if __name__ == "__main__":
    main()