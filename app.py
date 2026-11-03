# Import required libraries
from dotenv import load_dotenv  # For loading environment variables from .env file
import streamlit as st  # Streamlit library for creating the web application
import os  # For interacting with the operating system
import fitz  # PyMuPDF for high-speed local text extraction
from google import genai  # Modern Google GenAI SDK client
from google.genai import types  # Types for content generation

# Load environment variables from a .env file
load_dotenv()

# Helper Functions
def get_gemini_client():
    """Initialize and return the Google GenAI client."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Google API Key not found. Please add GOOGLE_API_KEY to your .env file.")
        return None
    return genai.Client(api_key=api_key)

def input_pdf_setup(uploaded_file):
    """
    Extract text locally from PDF using PyMuPDF (near-instant).
    Falls back to raw PDF bytes if the PDF is scanned / contains no selectable text.
    """
    pdf_bytes = uploaded_file.getvalue()
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc]).strip()
        doc.close()
        if text:
            return {"type": "text", "data": text}
    except Exception:
        pass
    
    # Fallback to raw PDF bytes for scanned documents
    return {"type": "pdf", "data": pdf_bytes}

def stream_gemini_response(input, pdf_data, prompt):
    """Stream response from the Google Gemini API chunk-by-chunk for near-instant rendering."""
    client = get_gemini_client()
    if not client:
        return
    
    contents = []
    if input:
        contents.append(f"Job Description:\n{input}")
    
    if pdf_data["type"] == "text":
        contents.append(f"Resume Content:\n{pdf_data['data']}")
    else:
        pdf_part = types.Part.from_bytes(
            data=pdf_data["data"],
            mime_type="application/pdf"
        )
        contents.append(pdf_part)
        
    contents.append(prompt)
    
    # Attempt streaming with modern active Flash models in order of availability and stability
    candidate_models = [
        'gemini-3.6-flash',
        'gemini-3.5-flash',
        'gemini-3.8-flash',
        'gemini-3.5-flash-lite'
    ]
    last_error = None
    for model_name in candidate_models:
        has_yielded = False
        try:
            response_stream = client.models.generate_content_stream(
                model=model_name,
                contents=contents
            )
            for chunk in response_stream:
                if chunk.text:
                    has_yielded = True
                    yield chunk.text
            return
        except Exception as e:
            last_error = e
            # If streaming already started yielding tokens to the UI, do not restart
            # with another model as that would produce duplicate/corrupted output.
            if has_yielded:
                raise e
            continue
    
    if last_error:
        raise last_error

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
        try:
            pdf_data = input_pdf_setup(uploaded_file)
            st.subheader("Evaluation Results")
            st.write_stream(stream_gemini_response(input_text, pdf_data, input_prompt1))
        except Exception as e:
            st.error(f"Error evaluating resume: {e}")
    else:
        st.error("Please upload a resume. ❌")

# Prompt 2: Percentage Match
if submit_match_eval:
    if uploaded_file:
        try:
            pdf_data = input_pdf_setup(uploaded_file)
            st.subheader("Percentage Match")
            st.write_stream(stream_gemini_response(input_text, pdf_data, input_prompt2))
        except Exception as e:
            st.error(f"Error calculating match percentage: {e}")
    else:
        st.error("Please upload a resume. ❌")

# Custom Prompt
if submit_custom_eval:
    if uploaded_file:
        if custom_prompt.strip():
            try:
                pdf_data = input_pdf_setup(uploaded_file)
                st.subheader("Custom Prompt Response")
                st.write_stream(stream_gemini_response(input_text, pdf_data, custom_prompt))
            except Exception as e:
                st.error(f"Error processing custom prompt: {e}")
        else:
            st.warning("Please provide a custom prompt. 📝")
    else:
        st.error("Please upload a resume. ❌")
