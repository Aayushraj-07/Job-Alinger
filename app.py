# Import required libraries
from dotenv import load_dotenv  # For loading environment variables from .env file
import base64  # For encoding binary data to base64
import streamlit as st  # Streamlit library for creating the web application
import os  # For interacting with the operating system
import io  # For handling byte streams
from PIL import Image  # Python Imaging Library for image processing
import fitz  # PyMuPDF for PDF processing
import google.generativeai as genai  # Google Generative AI API client

# Load environment variables from a .env file
load_dotenv()

# Configure the Google Gemini API with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Helper Functions
def input_pdf_setup(uploaded_file):
    """Convert uploaded PDF file to image format using PyMuPDF."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    first_page = doc[0]
    pix = first_page.get_pixmap()
    img_byte_arr = io.BytesIO()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    doc.close()
    return [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }
    ]

def get_gemini_response(input, pdf_content, prompt):
    """Generate a response from the Google Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Candidate Name, Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements in concise.
"""

input_prompt2 = """
You are a skilled Job Aligner scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as a percentage and then keywords missing and last final thoughts in concise.
"""

# Streamlit App Configuration
st.set_page_config(page_title="Job Aligner", page_icon=":guardsman:")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Job Aligner</h1>", unsafe_allow_html=True)

# Inject custom CSS to style the app
st.markdown("""
    <style>
        body {
            background-color: #fafafa;
            font-family: 'Arial', sans-serif;
            color: #333;
            line-height: 2;
        }
        .css-ffhzg2 {
            background-color: #4CAF50;
        }
        .stTextArea textarea {
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 12px;
            font-size: 16px;
        }
        .css-1d391kg {
            padding: 12px 25px;
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }
        .css-1d391kg:hover {
            background-color: #45a049;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 12px 25px;
            font-size: 16px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stAlert {
            background-color: #FFEB3B;
            color: #7F7F00;
        }
        .stWarning {
            background-color: #FFCC00;
            color: #6B6B00;
        }
        .stError {
            background-color: #FFCDD2;
            color: #B71C1C;
        }
        .stSuccess {
            background-color: #C8E6C9;
            color: #388E3C;
        }
        .stFileUploader {
            border: 2px dashed #4CAF50;
            padding: 10px;
            border-radius: 8px;
            background-color: #f1f1f1;
            transition: background-color 0.3s ease;
        }
        .stFileUploader:hover {
            background-color: #e8f5e9;
        }
    </style>
""", unsafe_allow_html=True)

# Input Fields
input_text = st.text_area("Job Description:", height=100, placeholder="Enter the job description here...")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])
custom_prompt = st.text_area("Write Your Custom Prompt:", height=80, placeholder="Provide a custom prompt for evaluation...")
submit_resume_eval = st.button("Tell Me About Resume")
submit_match_eval = st.button("Percentage Match")
submit_custom_eval = st.button("Use Custom Prompt")

if uploaded_file:
    st.success("Resume uploaded successfully! 🎉")

# Prompt 1: Evaluate Resume
if submit_resume_eval:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("Evaluation Results")
        st.write(response)
    else:
        st.error("Please upload a resume. ❌")

# Prompt 2: Percentage Match
if submit_match_eval:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("Percentage Match")
        st.write(response)
    else:
        st.error("Please upload a resume. ❌")

# Custom Prompt
if submit_custom_eval:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        if custom_prompt.strip():
            response = get_gemini_response(input_text, pdf_content, custom_prompt)
            st.subheader("Custom Prompt Response")
            st.write(response)
        else:
            st.warning("Please provide a custom prompt. 📝")
    else:
        st.error("Please upload a resume. ❌")
