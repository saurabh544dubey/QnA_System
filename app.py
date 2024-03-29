import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

#### Loading the environment variables---API
load_dotenv()

#### Configure the API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# -------------------------------------------------------------------------------------------------------------------------

#### Initializing the Models

# Text related tasks
model1 = genai.GenerativeModel("gemini-pro")
# Image data related tasks
model2 = genai.GenerativeModel("gemini-pro-vision")

# -------------------------------------------------------------------------------------------------------------------------

#### Initialize the Streamlit App
st.set_page_config(page_title="QnA Model" , page_icon=":page_with_curl:")

# -------------------------------------------------------------------------------------------------------------------------

#### Creating the App UI
# Title
st.title("QnA Model")
# Tabs
pro , pro_vision = st.tabs(["pro","vision_pro"])

# -------------------------------------------------------------------------------------------------------------------------

# Function to generate content
def generate_gemini_pro_response(user_input):
    response = model1.generate_content(user_input)
    return response.text

#### pro tab
user_input = pro.text_input("Ask any question" , key="pro_input" , placeholder="Provide the question here!")
submit = pro.button("Generate Response" , key="pro_button")

if submit:
    pro.success(generate_gemini_pro_response(user_input))

# -------------------------------------------------------------------------------------------------------------------------

# Function to handle image
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Check if the uploaded file is an image
        if uploaded_file.type.startswith('image'):
            # Read the file into bytes
            bytes_data = uploaded_file.read()
            
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data
                }
            ]
            return image_parts
        else:
            pro_vision.warning("Please upload a valid image file.")
    else:
        pro_vision.warning("No file uploaded.")

# Function to generate response
def generate_gemini_vision_response(input_text, image):
    response = model2.generate_content([input_text, image[0]])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Check if the uploaded file is an image
        if uploaded_file.type.startswith('image'):
            # Read the file into bytes
            bytes_data = uploaded_file.read()
            
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data
                }
            ]
            return image_parts
        else:
            pro_vision.warning("Please upload a valid image file.")
    else:
        pro_vision.warning("No file uploaded.")

#### pro-vision tab
input_prompt = pro_vision.text_input("Enter Prompt:", key="vision_input")
uploaded_file = pro_vision.file_uploader("Upload any Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display image
    pro_vision.subheader("Uploaded Image")
    pro_vision.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    
# Submit Button
submit = pro_vision.button("Generate Result",key="vision_button")

# Submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    if image_data:
        # Perform analysis
        response = generate_gemini_vision_response(input_prompt, image_data)
        
        # Display results
        pro_vision.subheader("Generated Result:")
        pro_vision.info(response)
