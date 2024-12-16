
                                               Job Aligner
                                               ___________


A Job Aligner based application that screens resumes against job descriptions, checks ATS compatibility, and provides personalized feedback to improve candidates’ resumes.

Table of Contents
1.	Overview
2.	Features
3.	Technologies Used
4.	Getting Started
     o	Prerequisites
     o	Setup Instructions
5.	Project Structure
6.	How to Use
________________________________________

Overview
--------

The Resume Screening Application helps recruiters and job seekers by analyzing resumes to determine how well they match job descriptions. It calculates a match percentage, identifies missing keywords, and provides feedback for improvements. This project uses Natural Language Processing (NLP) to analyze resume content and is integrated with Google Gemini API to generate contextual responses.

Features
--------

•	Resume Match Percentage: Calculates how well a resume aligns with a job description.
•	Keyword Matching & Feedback: Identifies key skills or terms missing from the resume.
•	ATS Compatibility Check: Ensures the resume meets common ATS standards.
•	Personalized Feedback: Provides suggestions for improving resume alignment with the job description.

Technologies Used
-----------------

•	Python: Backend programming language.
•	Streamlit: Web interface to run the application in the browser.
•	Google Gemini API: Provides contextual responses and feedback.
•	PDF2Image: Converts PDF resume files to images for processing.
•	dotenv: Loads environment variables for API keys.
•   pillow: Used for additional image processing, like saving and manipulating image formats before passing them  to the AI model.


Getting Started
---------------

Prerequisites:------

Before starting, ensure you have the following:
•	Python 3.8+ installed on your system.
•	A Google Gemini API Key for AI-based content generation.
•	Poppler library (for PDF2Image) if you're working with PDFs on Windows.

Setup Instructions:-----

1.	Clone the Repository: Download the code from the repository.

    bash
    Copy code
    git clone https://github.com/your-username/resume-screening-application.git
    cd resume-screening-application

2.	Set up a Virtual Environment (optional but recommended):

    bash
    Copy code
    python -m venv venv
    source venv/bin/activate   # On Windows use: venv\Scripts\activate

3.	Install Dependencies: Install the required Python libraries.

    bash
    Copy code
    pip install -r requirements.txt

4.	Configure API Key:

    o	Create a .env file in the root directory.
    o	Add your Google Gemini API key to the .env file:
    plaintext
    Copy code
    GOOGLE_API_KEY=your_api_key_here

5.	Install Poppler (for Windows users only):

o	Download Poppler for Windows here.
o	Extract the files and note the path (e.g., C:\path\to\poppler\bin).
o	Add this path to your PATH environment variable.
_____________________________________________________________________

Project Structure
-----------------

The main files and directories in this project:
•	app.py: Main Python script for running the application.
•	requirements.txt: List of required Python libraries.
•	.env: File containing environment variables (Google API Key).
•	README.md: Project documentation.

How to Use
----------

1.	Run the Application:
    o	Start the application with Streamlit:
        bash
        Copy code
        streamlit run app.py

2.	Using the Interface:

    •	Job Description: Enter the job description in the provided text box.
    •	Upload Resume: Upload a resume in PDF format.
    •	Analyze Options: Click the buttons for different analyses:
    •	Tell Me About the Resume: Provides a general analysis.
    •	Percentage Match: Calculates the match percentage and lists missing keywords.
    •   Custom Prompt 

3.	Results and Feedback:

    o	The app will display detailed feedback and recommendations for improving the resume.
________________________________________

Sample Code Breakdown
---------------------
Below is a breakdown of key functions in app.py:
•	get_gemini_response(): Sends job description and resume content to Google Gemini API for evaluation.
•	input_pdf_setup(): Converts the uploaded PDF to an image format compatible with the Google API.
•	Streamlit Buttons: Each button triggers different types of analysis and displays results.
________________________________________
Future Enhancements
•	Add more resume evaluation metrics.
•	Integrate with additional NLP libraries for deeper analysis.
•	Enable export options for analysis reports.

