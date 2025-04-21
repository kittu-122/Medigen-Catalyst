import streamlit as st
import os
import subprocess
import sys
import importlib

# Display installation status
st.set_page_config(page_title="MediGen Catalyst", page_icon="🩺")
st.title("Setting up dependencies...")

# Install required packages
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "google-generativeai"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "python-dotenv", "weasyprint"])

    st.success("Dependencies installed successfully!")
except Exception as e:
    st.error(f"Error installing dependencies: {str(e)}")
    st.info("Attempting to continue with existing packages...")

# Now import the packages
try:
    from PIL import Image
    from dotenv import load_dotenv
    import hashlib
    import google.generativeai as genai
    from weasyprint import HTML
    st.success("All required packages imported successfully!")
except ImportError as e:
    st.error(f"Failed to import: {str(e)}")
    st.stop()

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key exists
if not google_api_key:
    google_api_key = st.text_input("Enter your Google API Key:", type="password")
    if not google_api_key:
        st.warning("No API key found. Please enter your Google API key to continue.")
        st.stop()

# Configure AI Model
genai.configure(api_key=google_api_key)

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

# Updated System Prompt with Medications & Ointments
system_prompts = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the image.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured form.
3. Recommendation and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.
5. Medications & Ointments - If applicable, suggest medications (with dosage) and ointments based on the diagnosis.
6.  Home-Made Remedies - If suitable, provide safe and effective natural remedies that may help alleviate symptoms.

⚠️ Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Only provide medications if there is a clear diagnosis.
3. Ensure that your recommendations align with standard medical practices.
4. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
5. Home-made remedies should be **safe, simple, and widely recognized** (e.g., warm compress, turmeric milk, saline rinse).
6. Disclaimer: Accompany your analysis with the disclaimer "Consult with a Doctor before making any decisions."
7. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.


Please provide me an output response with these 4 headings Detailed Analysis,Findings Report,Recommendation and Next Steps,Treatment Suggestions, medications and ointments, home-made remedies 
"""

# Remove the setup-related UI now that dependencies are installed
if st.session_state.get("show_main_app") is None:
    st.session_state.show_main_app = True
    st.rerun()

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "📂 Upload & Analyze", "💬 Ask AI", "🕘 Previous Interactions", "ℹ️ How It Works"])

# Initialize session states
if "analyses" not in st.session_state:
    st.session_state.analyses = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# Function to generate and download PDF reports
def generate_pdf(report_text, filename="analysis_report.pdf"):
    try:
        HTML(string=report_text).write_pdf(filename)
        return filename
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None

# Function to hash images (for deduplication)
def hash_image(image):
    try:
        image_bytes = image.tobytes()
        return hashlib.md5(image_bytes).hexdigest()
    except Exception as e:
        st.error(f"Error hashing image: {str(e)}")
        return None

# ------------------- HOME PAGE -------------------
if page == "🏠 Home":
    st.title("🏥 Welcome to MediGen Catalyst")
    st.write("An AI-powered platform for **medical image analysis**. Upload an image, get insights, and ask follow-up questions.")
    
    # Check if image exists, if not show placeholder text
    try:
        st.image("medigencat.png", width=200)
    except:
        st.warning("Logo image not found. Please add 'medigencat.png' to your app directory.")
    
    st.info("🔹 Use the sidebar to upload images or ask AI questions.")

# ------------------- UPLOAD & ANALYZE -------------------
elif page == "📂 Upload & Analyze":
    st.title("📂 Upload & Analyze Medical Images")
    
    # File uploader
    uploaded_files = st.file_uploader("Upload medical images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        processed_images = {}
        unique_images = []

        for uploaded_file in uploaded_files:
            try:
                image = Image.open(uploaded_file)
                st.image(image, width=150, caption=f"Uploaded: {uploaded_file.name}")

                image_hash = hash_image(image)
                if image_hash and image_hash not in processed_images:
                    processed_images[image_hash] = uploaded_file
                    unique_images.append(image_hash)
            except Exception as e:
                st.error(f"Error processing image {uploaded_file.name}: {str(e)}")

        for image_hash in unique_images:
            primary_file = processed_images[image_hash]

            if st.button(f"🔬 Analyze {primary_file.name}"):
                st.session_state.selected_image = primary_file  # Store the image for follow-up questions
                progress_bar = st.progress(0)

                try:
                    image_data = primary_file.getvalue()
                    image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
                    prompt_parts = [image_parts[0], system_prompts]

                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-pro-latest",
                        generation_config=generation_config,
                        safety_settings=safety_settings,
                    )

                    with st.spinner("🔎 Analyzing..."):
                        response = model.generate_content(prompt_parts)
                        progress_bar.progress(50)

                    if response and response.text:
                        analysis_text = response.text
                        st.write(f"### 📝 Analysis for {primary_file.name}")
                        st.write(analysis_text)
                        st.session_state.analyses[primary_file.name] = analysis_text
                        progress_bar.progress(100)

                        # Generate and provide download link for report
                        pdf_filename = generate_pdf(analysis_text)
                        if pdf_filename:
                            with open(pdf_filename, "rb") as pdf_file:
                                st.download_button(label="📥 Download Report", data=pdf_file, file_name=pdf_filename, mime="application/pdf")
                    else:
                        st.error("❌ Failed to generate analysis. Please try again.")
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    progress_bar.progress(100)

    # 🔹 Show previous analyses below images
    if st.session_state.analyses:
        st.subheader("🔍 Previous Analyses")
        for image_name, analysis_text in st.session_state.analyses.items():
            with st.expander(f"Analysis for {image_name}"):
                st.write(analysis_text)

    # 🔹 Button to clear analysis history
    if st.button("🗑️ Clear Analysis History"):
        st.session_state.analyses = {}
        st.rerun()

# ------------------- ASK AI (CHATBOT) -------------------
elif page == "💬 Ask AI":
    st.title("💬 Ask AI About Your Analysis")

    if not st.session_state.selected_image:
        st.warning("Please analyze an image first in 'Upload & Analyze' before asking AI.")
    else:
        try:
            selected_image = st.session_state.selected_image
            analysis_text = st.session_state.analyses.get(selected_image.name, "No analysis available.")

            # Show the analyzed image and its report
            st.image(selected_image, width=200, caption=f"Current Image: {selected_image.name}")
            st.write(f"### 📝 Analysis for {selected_image.name}")
            st.write(analysis_text)

            # Display chat history
            chat_container = st.container()
            for q, r in st.session_state.chat_history:
                with chat_container:
                    st.markdown(f"**🧑‍⚕️ User:** {q}")
                    st.markdown(f"**🤖 AI:** {r}")

            # Input for AI follow-up questions
            question = st.text_input("💡 Ask a follow-up question:", key="chat_input")

            if st.button("Ask AI") and question:
                try:
                    chatbot_prompt = f"Based on the previous analysis: {analysis_text}, answer this question: {question}"
                    model = genai.GenerativeModel(
                        model_name="gemini-1.5-pro-latest",
                        generation_config=generation_config,
                        safety_settings=safety_settings,
                    )

                    with st.spinner("🤖 Thinking..."):
                        chatbot_response = model.generate_content(chatbot_prompt)

                    if chatbot_response and chatbot_response.text:
                        st.session_state.chat_history.append((question, chatbot_response.text))
                        st.rerun()
                    else:
                        st.error("Failed to get a response from AI. Please try again.")
                except Exception as e:
                    st.error(f"Error during AI conversation: {str(e)}")
        except Exception as e:
            st.error(f"Error displaying analysis: {str(e)}")

# ------------------- PREVIOUS INTERACTIONS -------------------
elif page == "🕘 Previous Interactions":
    st.title("🕘 Previous AI Interactions")

    if not st.session_state.chat_history:
        st.info("No previous interactions found. Ask a follow-up question in 'Ask AI'!")
    else:
        for q, r in st.session_state.chat_history:
            st.markdown(f"**🧑‍⚕️ User:** {q}")
            st.markdown(f"**🤖 AI:** {r}")

    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# ------------------- HOW IT WORKS -------------------
elif page == "ℹ️ How It Works":
    st.title("ℹ️ How MediGen Catalyst Works")
    st.write("""
    - Upload medical images  
    - AI generates a **detailed diagnostic report**  
    - AI recommends **medications & ointments**  
    - Ask follow-up questions  
    """)
    
    # Check if image exists, if not show placeholder text
    try:
        st.image("workflow_diagram.png", caption="Working of Medigen-Catalyst")
    except:
        st.warning("Workflow diagram not found. Please add 'workflow_diagram.png' to your app directory.")
