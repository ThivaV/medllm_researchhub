import streamlit as st  # type: ignore
import tempfile
from PIL import Image

def initialize():
    """BioMED ⚕️ VisionLM AI Tool initialization"""
    st.title("BioMEDICAL VisionLM AI Tool")
    st.info(
        "🚨 This application is designed as a comprehensive AI tool for medical analysis, leveraging advanced multimodal capabilities to assist healthcare professionals and potentially extend access to underserved communities."
    )

    # File uploader for both images and PDFs
    uploaded_files = st.file_uploader(
        "Choose files...",
        type=["jpg", "png", "jpeg", "pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:

            for uploaded_file in uploaded_files:
                # Write the uploaded file's contents to the temporary file
                temp_file.write(uploaded_file.getbuffer())

                # Get the temporary file path
                temp_file_path = temp_file.name
                st.write(f"File saved temporarily at: {temp_file_path}")

                # If the file is an image, display it
                if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
                    image = Image.open(temp_file_path)
                    st.image(image, caption='Uploaded Image', width=500)
                    
                # If the file is a PDF, display a message (you can implement further handling if needed)
                elif uploaded_file.type == "application/pdf":
                    st.write("Uploaded PDF file.")
