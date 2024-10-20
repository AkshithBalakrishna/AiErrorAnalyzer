import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2 as pdf
from PIL import Image
import io
import json  # For checking JSON validity

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from the Gemini model
def get_gemini_response(input_text, input_image=None):
    model = genai.GenerativeModel('gemini-pro' if input_image is None else 'gemini-1.5-flash')
    if input_image:
        response = model.generate_content([input_text, input_image])
    else:
        response = model.generate_content(input_text)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Function to extract text from a .txt file
def input_txt_text(uploaded_file):
    stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    return stringio.read()

# Function to check if the response is valid JSON
def is_json(response):
    try:
        json.loads(response)
        return True
    except ValueError:
        return False

# Streamlit UI components
st.title("Error Analyzer")
st.text("Upload your error message, screenshot, or log for analysis")

# Input type selection
input_type = st.radio("Select input type:", ("Text", "Image", "PDF", "Text File (.txt)"))

# Text input or file upload based on input type selection
if input_type == "Text":
    user_input = st.text_area("Paste your error message or code snippet here:")
    file_input = None
elif input_type == "Image":
    file_input = st.file_uploader("Upload an image of your error", type=["png", "jpg", "jpeg"])
    user_input = None
elif input_type == "PDF":
    file_input = st.file_uploader("Upload your error log or code file (PDF)", type="pdf")
    user_input = None
else:
    file_input = st.file_uploader("Upload your error log or code file (.txt)", type="txt")
    user_input = None

# Input prompt template for error analysis
input_prompt = """
As an expert in API troubleshooting and code debugging, your role is to analyze errors, diagnose their root causes, and provide clear explanations and solutions. When presented with an error:

1. Carefully examine the error message, status code (if applicable), and any additional context provided.
2. Identify the type of error (e.g., API-related, syntax error, runtime error, logical error).
3. Explain the error in simple terms, avoiding overly technical jargon.
4. Suggest potential causes for the error, considering common pitfalls and best practices.
5. Provide step-by-step troubleshooting instructions, including how to:
   - Verify API credentials and authentication (if applicable)
   - Check request formatting and parameters (for API errors)
   - Validate data being sent or processed
   - Test API endpoints or specific code sections
   - Review logs or error messages
6. Recommend tools or techniques for debugging (e.g., API testing tools, logging, debuggers, print statements).
7. Offer potential solutions or workarounds for the error.
8. If relevant, suggest preventive measures to avoid similar errors in the future.
9. Be prepared to explain API concepts, HTTP methods, status codes, and common programming concepts as needed.
10. If the error seems unique or complex, provide resources for further research or suggest escalation paths.

Error details:
{input_text}

Please provide a comprehensive analysis and solution in this format:
  "Error Type": "",
  "Explanation": "",
  "Potential Causes": [],
  "Troubleshooting Steps": [],
  "Recommended Tools": [],
  "Potential Solutions": [],
  "Preventive Measures": [],
  "Additional Resources": []
"""

# Analyze button to trigger error analysis
submit = st.button("Analyze")

# Error analysis logic
if submit:
    if input_type == "Text" and user_input:
        # Text input analysis
        response = get_gemini_response(input_prompt.format(input_text=user_input))
        
        # Check if response is valid JSON
        if is_json(response):
            st.json(json.loads(response))
        else:
            st.text_area("Response (Text)", response)
    
    elif input_type == "Image" and file_input:
        # Image input analysis
        image = Image.open(file_input)
        response = get_gemini_response(input_prompt.format(input_text="Analyze the error in this image:"), image)
        
        # Check if response is valid JSON
        if is_json(response):
            st.json(json.loads(response))
        else:
            st.text_area("Response (Text)", response)
    
    elif input_type == "PDF" and file_input:
        # PDF input analysis
        text = input_pdf_text(file_input)
        response = get_gemini_response(input_prompt.format(input_text=text))
        
        # Check if response is valid JSON
        if is_json(response):
            st.json(json.loads(response))
        else:
            st.text_area("Response (Text)", response)

    elif input_type == "Text File (.txt)" and file_input:
        # Text file (.txt) input analysis
        text = input_txt_text(file_input)
        response = get_gemini_response(input_prompt.format(input_text=text))
        
        # Check if response is valid JSON
        if is_json(response):
            st.json(json.loads(response))
        else:
            st.text_area("Response (Text)", response)
    
    else:
        st.error("Please provide input based on your selected input type.")


# ---------------------------------------------------------


# import streamlit as st
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# import PyPDF2 as pdf
# from PIL import Image
# import io
# import json  # For checking JSON validity

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Custom CSS for professional look
# def add_custom_css():
#     st.markdown(
#         """
#         <style>
#         /* General App Background */
#         .stApp {
#             background-color: #F7F7F7;
#             color: #333333;
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         }

#         /* Headers Styling */
#         h1, h2, h3, h4, h5, h6 {
#             color: #2C3E50;
#             font-weight: 600;
#             border-bottom: 2px solid #E7E7E7;
#             padding-bottom: 10px;
#             margin-bottom: 20px;
#         }

#         /* Radio buttons styling */
#         .stRadio label {
#             font-weight: 500;
#             color: #34495E;
#         }

#         /* Text area styling */
#         textarea {
#             background-color: #FFFFFF;
#             color: #34495E;
#             border: 1px solid #BDC3C7;
#             border-radius: 8px;
#             padding: 10px;
#             transition: border-color 0.3s ease-in-out;
#         }
#         textarea:focus {
#             border-color: #2980B9;
#             outline: none;
#         }

#         /* File uploader styling */
#         .stFileUploader {
#             background-color: #ECF0F1;
#             border: 2px dashed #BDC3C7;
#             border-radius: 8px;
#             padding: 20px;
#             margin-bottom: 20px;
#         }

#         /* Button styling */
#         div.stButton > button {
#             background-color: #3498DB;
#             color: #FFFFFF;
#             font-size: 16px;
#             font-weight: 600;
#             border: none;
#             border-radius: 6px;
#             padding: 12px 24px;
#             cursor: pointer;
#             transition: background-color 0.3s ease-in-out;
#         }
#         div.stButton > button:hover {
#             background-color: #2980B9;
#         }

#         /* Style for text area and JSON output */
#         .stTextArea, .stJson {
#             background-color: #FFFFFF;
#             color: #2C3E50;
#             border: 1px solid #BDC3C7;
#             border-radius: 8px;
#             padding: 15px;
#             margin-top: 10px;
#         }

#         /* Global padding */
#         .stApp > div {
#             padding: 40px;
#         }

#         /* Block container for centering and layout control */
#         .block-container {
#             padding: 40px 40px;
#             background-color: #FFFFFF;
#             box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
#             border-radius: 8px;
#             max-width: 800px;
#             margin: 0 auto;
#         }

#         /* Inputs and text areas */
#         input[type="text"], input[type="email"], textarea {
#             border: 1px solid #BDC3C7;
#             border-radius: 4px;
#             padding: 12px;
#             margin-top: 10px;
#             width: 100%;
#         }

#         /* Improve accessibility by focusing on form controls */
#         input:focus, textarea:focus {
#             border-color: #2980B9;
#         }

#         /* Horizontal rules for separators */
#         hr {
#             border-top: 1px solid #E7E7E7;
#             margin: 30px 0;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # Add the custom CSS
# add_custom_css()



# # Function to get response from the Gemini model
# def get_gemini_response(input_text, input_image=None):
#     model = genai.GenerativeModel('gemini-pro' if input_image is None else 'gemini-1.5-flash')
#     if input_image:
#         response = model.generate_content([input_text, input_image])
#     else:
#         response = model.generate_content(input_text)
#     return response.text

# # Function to extract text from PDF
# def input_pdf_text(uploaded_file):
#     reader = pdf.PdfReader(uploaded_file)
#     text = ""
#     for page in reader.pages:
#         text += str(page.extract_text())
#     return text

# # Function to extract text from a .txt file
# def input_txt_text(uploaded_file):
#     stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
#     return stringio.read()

# # Function to check if the response is valid JSON
# def is_json(response):
#     try:
#         json.loads(response)
#         return True
#     except ValueError:
#         return False

# # Streamlit UI components
# st.title("Error Analyzer")
# st.text("Upload your error message, screenshot, or log for analysis")

# # Input type selection
# input_type = st.radio("Select input type:", ("Text", "Image", "PDF", "Text File (.txt)"))

# # Text input or file upload based on input type selection
# if input_type == "Text":
#     user_input = st.text_area("Paste your error message or code snippet here:")
#     file_input = None
# elif input_type == "Image":
#     file_input = st.file_uploader("Upload an image of your error", type=["png", "jpg", "jpeg"])
#     user_input = None
# elif input_type == "PDF":
#     file_input = st.file_uploader("Upload your error log or code file (PDF)", type="pdf")
#     user_input = None
# else:
#     file_input = st.file_uploader("Upload your error log or code file (.txt)", type="txt")
#     user_input = None

# # Input prompt template for error analysis
# input_prompt = """
# As an expert in API troubleshooting and code debugging, your role is to analyze errors, diagnose their root causes, and provide clear explanations and solutions. When presented with an error:

# 1. Carefully examine the error message, status code (if applicable), and any additional context provided.
# 2. Identify the type of error (e.g., API-related, syntax error, runtime error, logical error).
# 3. Explain the error in simple terms, avoiding overly technical jargon.
# 4. Suggest potential causes for the error, considering common pitfalls and best practices.
# 5. Provide step-by-step troubleshooting instructions, including how to:
#    - Verify API credentials and authentication (if applicable)
#    - Check request formatting and parameters (for API errors)
#    - Validate data being sent or processed
#    - Test API endpoints or specific code sections
#    - Review logs or error messages
# 6. Recommend tools or techniques for debugging (e.g., API testing tools, logging, debuggers, print statements).
# 7. Offer potential solutions or workarounds for the error.
# 8. If relevant, suggest preventive measures to avoid similar errors in the future.
# 9. Be prepared to explain API concepts, HTTP methods, status codes, and common programming concepts as needed.
# 10. If the error seems unique or complex, provide resources for further research or suggest escalation paths.

# Error details:
# {input_text}

# Please provide a comprehensive analysis and solution in this format:
#   "Error Type": "",
#   "Explanation": "",
#   "Potential Causes": [],
#   "Troubleshooting Steps": [],
#   "Recommended Tools": [],
#   "Potential Solutions": [],
#   "Preventive Measures": [],
#   "Additional Resources": []
# """

# # Analyze button to trigger error analysis
# submit = st.button("Analyze")

# # Error analysis logic
# if submit:
#     if input_type == "Text" and user_input:
#         # Text input analysis
#         response = get_gemini_response(input_prompt.format(input_text=user_input))
        
#         # Check if response is valid JSON
#         if is_json(response):
#             st.json(json.loads(response))
#         else:
#             st.text_area("Response (Text)", response)
    
#     elif input_type == "Image" and file_input:
#         # Image input analysis
#         image = Image.open(file_input)
#         response = get_gemini_response(input_prompt.format(input_text="Analyze the error in this image:"), image)
        
#         # Check if response is valid JSON
#         if is_json(response):
#             st.json(json.loads(response))
#         else:
#             st.text_area("Response (Text)", response)
    
#     elif input_type == "PDF" and file_input:
#         # PDF input analysis
#         text = input_pdf_text(file_input)
#         response = get_gemini_response(input_prompt.format(input_text=text))
        
#         # Check if response is valid JSON
#         if is_json(response):
#             st.json(json.loads(response))
#         else:
#             st.text_area("Response (Text)", response)

#     elif input_type == "Text File (.txt)" and file_input:
#         # Text file (.txt) input analysis
#         text = input_txt_text(file_input)
#         response = get_gemini_response(input_prompt.format(input_text=text))
        
#         # Check if response is valid JSON
#         if is_json(response):
#             st.json(json.loads(response))
#         else:
#             st.text_area("Response (Text)", response)
    
#     else:
#         st.error("Please provide input based on your selected input type.")


# # -------------------------------------------------


# import streamlit as st
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# import requests  # For HTTP calls to the SAP CPI
# import PyPDF2 as pdf
# from PIL import Image
# import io
# import json  # For checking JSON validity
# from requests.auth import HTTPBasicAuth  # For Basic Authentication

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Base URL for SAP CPI IFlow request-reply calls
# SAP_CPI_BASE_URL = "https://e1b8acf4trial.it-cpitrial05-rt.cfapps.us10-001.hana.ondemand.com/http/error1"

# # Custom CSS for professional look
# def add_custom_css():
#     st.markdown(
#         """
#         <style>
#         /* General App Background */
#         .stApp {
#             background-color: #F7F7F7;
#             color: #333333;
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         }

#         /* Headers Styling */
#         h1, h2, h3, b {
#             color: #2C3E50;
#             font-weight: 600;
#             border-bottom: 2px solid #E7E7E7;
#             padding-bottom: 10px;
#             margin-bottom: 20px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # Add the custom CSS
# add_custom_css()

# # Function to get response from the Gemini model
# def get_gemini_response(input_text, input_image=None):
#     model = genai.GenerativeModel('gemini-pro' if input_image is None else 'gemini-1.5-flash')
#     if input_image:
#         response = model.generate_content([input_text, input_image])
#     else:
#         response = model.generate_content(input_text)
#     return response.text

# # Function to extract text from PDF
# def input_pdf_text(uploaded_file):
#     reader = pdf.PdfReader(uploaded_file)
#     text = ""
#     for page in reader.pages:
#         text += str(page.extract_text())
#     return text

# # Function to extract text from a .txt file
# def input_txt_text(uploaded_file):
#     stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
#     return stringio.read()

# # Function to check if the response is valid JSON
# def is_json(response):
#     try:
#         json.loads(response)
#         return True
#     except ValueError:
#         return False

# # Function to send error details to SAP CPI (POST) with Basic Authentication
# def send_error_to_sap_cpi(error_details):
#     url = SAP_CPI_BASE_URL  # POST URL for request-reply IFlow
#     headers = {'Content-Type': 'application/json'}
    
#     # Replace with your SAP CPI credentials
#     username = 'your_username'  # Replace with your actual username
#     password = 'your_password'  # Replace with your actual password

#     # Make the POST request with basic authentication
#     response = requests.post(
#         url,
#         data=json.dumps(error_details),
#         headers=headers,
#         auth=HTTPBasicAuth(username, password),  # Basic Authentication
#         timeout=30
#     )
    
#     return response.status_code, response.text

# # Function to fetch error details from SAP CPI (GET) with Basic Authentication
# def fetch_error_from_sap_cpi(error_id):
#     url = f"{SAP_CPI_BASE_URL}/{error_id}"  # GET URL for request-reply IFlow
    
#     # Replace with your SAP CPI credentials
#     username = 'your_username'  # Replace with your actual username
#     password = 'your_password'  # Replace with your actual password

#     # Make the GET request with basic authentication
#     response = requests.get(
#         url,
#         auth=HTTPBasicAuth(username, password),  # Basic Authentication
#         timeout=30
#     )
    
#     return response.status_code, response.text

# # Streamlit UI components
# st.title("Error Analyzer")
# st.text("Upload your error message, screenshot, or log for analysis")

# # Input type selection
# input_type = st.radio("Select input type:", ("Text", "Image", "PDF", "Text File (.txt)"))

# # Text input or file upload based on input type selection
# if input_type == "Text":
#     user_input = st.text_area("Paste your error message or code snippet here:")
#     file_input = None
# elif input_type == "Image":
#     file_input = st.file_uploader("Upload an image of your error", type=["png", "jpg", "jpeg"])
#     user_input = None
# elif input_type == "PDF":
#     file_input = st.file_uploader("Upload your error log or code file (PDF)", type="pdf")
#     user_input = None
# else:
#     file_input = st.file_uploader("Upload your error log or code file (.txt)", type="txt")
#     user_input = None

# # Input prompt template for error analysis
# input_prompt = """
# As an expert in API troubleshooting and code debugging, your role is to analyze errors, diagnose their root causes, and provide clear explanations and solutions.

# Error details:
# {input_text}

# Please provide a comprehensive analysis and solution.
# """

# # Analyze button to trigger error analysis
# submit = st.button("Analyze")

# # Error analysis logic
# if submit:
#     if input_type == "Text" and user_input:
#         # Text input analysis
#         response = get_gemini_response(input_prompt.format(input_text=user_input))

#         # Send error details to SAP CPI using POST
#         error_details = {
#             "input_text": user_input,
#             "analysis": response
#         }
#         status_code, post_response = send_error_to_sap_cpi(error_details)
        
#         # Display SAP CPI response
#         st.write(f"POST Response Code: {status_code}")
#         st.text_area("POST Response", post_response)

#         # Optionally fetch the error details using GET
#         fetch = st.button("Fetch Error Details (GET)")
#         if fetch:
#             error_id = "some-error-id"  # Replace with your logic to retrieve error_id
#             status_code, get_response = fetch_error_from_sap_cpi(error_id)
#             st.write(f"GET Response Code: {status_code}")
#             st.text_area("GET Response", get_response)
    
#     elif input_type == "Image" and file_input:
#         # Image input analysis
#         image = Image.open(file_input)
#         response = get_gemini_response(input_prompt.format(input_text="Analyze the error in this image:"), image)

#         # Send and fetch error as shown for text case
#         # Follow same logic for POST and GET handling for image input

#     elif input_type == "PDF" and file_input:
#         # PDF input analysis
#         text = input_pdf_text(file_input)
#         response = get_gemini_response(input_prompt.format(input_text=text))

#         # Send and fetch error as shown for text case
#         # Follow same logic for POST and GET handling for PDF input

#     elif input_type == "Text File (.txt)" and file_input:
#         # Text file (.txt) input analysis
#         text = input_txt_text(file_input)
#         response = get_gemini_response(input_prompt.format(input_text=text))

#         # Send and fetch error as shown for text case
#         # Follow same logic for POST and GET handling for .txt input
    
#     else:
#         st.error("Please provide input based on your selected input type.")
