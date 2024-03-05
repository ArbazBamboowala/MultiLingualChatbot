# Q&A Chatbot
#from langchain.llms import OpenAI
##streamlit run c:/Users/arbaz/Documents/MultiLangModel/app.py
##CURRENT DIR: C:\Users\arbaz\AppData\Roaming\Python\Python39\Scripts>
##Command to run : streamlit run C:\Users\arbaz\Documents\MultiLangModel\app.py
##activate conda: C:/tools/Anaconda3/Scripts/activate
#conda activate c:\Users\arbaz\Documents\MultiLangModel\venv
# Q&A Chatbot
#from langchain.llms import OpenAI
from dotenv import load_dotenv
from io import BytesIO
import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Generative AI
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to handle uploaded file input
def input_file_setup(uploaded_file):
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue()
        if uploaded_file.type == "application/pdf":
            # PDF input
            doc = fitz.open(stream=BytesIO(file_content))
            pdf_text = ""
            for page in doc:
                pdf_text += page.get_text()
            return pdf_text if pdf_text else "No text found in the PDF."
        else:
            # Image input
            image = Image.open(BytesIO(file_content))
            return [image]

# Function to check login credentials
def check_login(username, password):
    return username == "your_username" and password == "your_password"

# Streamlit UI
st.set_page_config(page_title="Multi Lingual Image Document based Chat Bot")
st.title("Multi Lingual Image Document based Chat Bot")

# Create session state
session_state = st.session_state
if not hasattr(session_state, "logged_in"):
    session_state.logged_in = False

# Sidebar for Login
st.sidebar.title("Login")
username = st.sidebar.text_input("Username", key="username")
password = st.sidebar.text_input("Password", key="password", type="password")

login_button = st.sidebar.button("Login")

# Check login credentials
if login_button and check_login(username, password):
    # User is logged in, display the main content
    session_state.logged_in = True

# Logout button
logout_button = st.button("Logout")

# If logout button is clicked
if logout_button:
    session_state.logged_in = False

# Check if user is logged in
if session_state.logged_in:
    input_prompt = """
                   You are an expert in understanding official documents including passports, bank statements, Identification card, driving license, state id in any language.
                   You will receive input images as official documents including passports, bank statements, Identification card, driving license, state id in any language &
                   you will have to answer questions based on the input.
                   """

    # User input fields
    input_text = st.text_input("Input Prompt: ", key="input")
    uploaded_file = st.file_uploader("Upload an image or PDF...", type=["jpg", "jpeg", "png"])

    # Submit button
    submit = st.button("Tell me about the file")

    # If submit button is clicked
    if submit:
        file_data = input_file_setup(uploaded_file)
        response = get_gemini_response(input_prompt, file_data, input_text)
        st.subheader("The Response is")
        st.write(response)

else:
    # User is not logged in, display a login prompt
    st.sidebar.warning("Incorrect username or password. Please try again.")
