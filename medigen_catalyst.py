import streamlit as st
from PIL import Image
from google.cloud import aiplatform
from api_key import api_key
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
aiplatform.init(project="medical", location="us-central1")

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System prompts
system_prompts = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the image.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured form.
3. Recommendation and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer "Consult with a Doctor before making any decisions."
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide me an output response with these 4 headings Detailed Analysis,Findings Report,Recommendation and Next Steps,Treatment Suggestions
"""

# system_prompts = """
# As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues present in these images.

# Your Responsibilities include:

# 1. Detailed Analysis:Thoroughly analyze each image.
#                      Focus on identifying any abnormal findings.
# 2. Findings Report: Document all observed anomalies or signs of disease.
#                     Clearly articulate these findings in a structured form.
# 3. Recommendations and Next Steps:Based on your analysis, suggest potential next steps.
#                         Include recommendations for further tests or treatments as applicable.
# 4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

# Important Notes:

# 1. Scope of Response: Only respond if the image pertains to human health issues.
# 2. Clarity of Image: If the image quality impedes clear analysis, note that certain aspects are "Unable to be determined based on the provided image"
# 3. Disclaimer:

# Accompany your analysis with the disclaimer: "Consult with a doctor before making any decisions."
# Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.
# """

# Create a unique interface
st.set_page_config(page_title="MediGen Catalyst", page_icon=":microscope:")

st.image("medigencat.png" , width=150)

# Header
st.title("Welcome to MediGen Catalyst")
st.subheader("An application that helps analyze medical images")
# Upload image
uploaded_file = st.file_uploader("Upload a medical image for analysis", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, width=300, caption="Uploaded Medical Image")

    # Analysis button
    if st.button("Generate Analysis"):
        # Placeholder for progress bar
        progress_bar = st.progress(0)
        progress_text = st.empty()

        # Prepare image data
        image_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]

        # Generate analysis
        prompt_parts = [image_parts[0], system_prompts]
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config,
                                      safety_settings=safety_settings)

        with st.spinner("Analyzing..."):
            response = model.generate_content(prompt_parts)

        # Display analysis
        if response:
            progress_bar.progress(100)
            progress_text.text("Analysis Complete!")
            st.title("Here is the analysis based on your image: ")
            st.write(response.text)
else:
    st.warning("Please upload an image for analysis.")
