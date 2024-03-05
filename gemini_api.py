from flask import Flask, request, jsonify
from llmsherpa.readers import LayoutPDFReader
from vertexai.preview.generative_models import GenerativeModel
import os

app = Flask(__name__)

# Set up Gemini Pro API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"./c:\Users\arbaz\Downloads\arbazgcpcred.json"

# Function to extract text from a PDF URL
# Function to extract text from a PDF URL
def extract_text_from_pdf(pdf_url):
    llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
    pdf_reader = LayoutPDFReader(llmsherpa_api_url)
    doc = {}  # Initialize an empty dictionary

    try:
        doc = pdf_reader.read_pdf(pdf_url)
        blocks = doc.get('return_dict', {}).get('result', {}).get('blocks', [])
        text = "\n".join([block['text'] for block in blocks])
        return text
    except KeyError as e:
        error_message = f"KeyError: {e}. JSON response: {doc}"
        print(error_message)
        return f"Error extracting text from PDF: {error_message}"
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return f"Error extracting text from PDF: {error_message}"


# Function to get Gemini Pro response
def get_gemini_response(prompt_text):
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(prompt_text, stream=False)
    return response.candidates[0].content.parts[0].text

# Endpoint to process PDF and respond to prompts
@app.route('/process_pdf_and_respond', methods=['POST'])
def process_pdf_and_respond():
    data = request.get_json()
    pdf_url = data.get('pdf_url')
    prompt_text = data.get('prompt_text')

    if not pdf_url or not prompt_text:
        return jsonify({'error': 'Missing PDF URL or prompt text'})

    pdf_text = extract_text_from_pdf(pdf_url)
    response = get_gemini_response(f"{prompt_text}\n{pdf_text}")

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
