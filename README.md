# Job Aligner

An AI-powered Job Aligner application that screens resumes against job descriptions, checks ATS compatibility, and provides personalized feedback to improve candidates’ resumes with real-time response streaming.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Setup Instructions](#setup-instructions)
5. [Project Structure](#project-structure)
6. [How to Use](#how-to-use)
7. [Future Enhancements](#future-enhancements)

---

## Overview

The **Job Aligner** application helps recruiters and job seekers by analyzing resumes to determine how well they match job descriptions. It calculates match percentages, identifies missing keywords, checks ATS standards, and provides actionable recommendations. The project is integrated with Google's Gemini API via the official `google-genai` SDK for high-speed analysis and real-time streaming feedback.

---

## Features

- **Resume Match Percentage**: Calculates how well a resume aligns with a job description.
- **Keyword Matching & Feedback**: Identifies key skills or terms missing from the resume.
- **ATS Compatibility Check**: Ensures the resume meets modern ATS standards.
- **Personalized HR Evaluation**: Highlights applicant strengths and weaknesses in relation to specific job requirements.
- **Custom Prompts**: Allows users to run tailored evaluations and questions against the resume and job description.
- **High-Speed Streaming**: Streams model responses in real-time with sub-second perceived latency.
- **Multi-Page Support**: Reads and processes entire multi-page resumes cleanly via high-speed local PDF parsing.

---

## Technologies Used

- **Python**: Backend programming language.
- **Streamlit**: Fast web application framework.
- **Google GenAI SDK (`google-genai`)**: Interfacing with Google Gemini Flash models.
- **PyMuPDF (`fitz`)**: Fast, lightweight local text extraction from PDF files.
- **python-dotenv**: Managing environment variables for API keys.

---

## Getting Started

### Prerequisites
- Python 3.8+ installed on your system.
- A Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Aayushraj-07/Job-Alinger.git
   cd Job-Alinger
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**:
   Create a `.env` file in the root directory and add your key:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

---

## Project Structure

```text
├── .devcontainer/         # Dev container configuration for Codespaces / Docker
├── app.py                 # Main Streamlit application and Gemini workflow
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (excluded from git)
└── README.md              # Project documentation
```

---

## How to Use

1. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

2. **Using the Interface**:
   - **Job Description**: Enter or paste the job description.
   - **Upload Resume**: Upload your resume in PDF format.
   - **Choose Analysis**:
     - *Tell Me About Resume*: Comprehensive HR manager review.
     - *Percentage Match*: ATS alignment score and missing keywords.
     - *Use Custom Prompt*: Custom query or prompt against the resume.

---

## Future Enhancements
- Add export options (PDF / Markdown report downloads).
- Interactive keyword visualization and scoring charts.
- Support for Word document formats (.docx).
