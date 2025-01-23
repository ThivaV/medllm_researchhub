import streamlit as st
import tempfile
import os
from PIL import Image

st.title('Upload Files to Temporary Location')

# File uploader for both images and PDFs
uploaded_file = st.file_uploader("Choose a file...", type=["jpg", "png", "jpeg", "pdf"])

if uploaded_file is not None:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        # Write the uploaded file's contents to the temporary file
        temp_file.write(uploaded_file.getbuffer())
        
        # Get the temporary file path
        temp_file_path = temp_file.name
        st.write(f"File saved temporarily at: {temp_file_path}")

    # If the file is an image, display it
    if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
        image = Image.open(temp_file_path)
        st.image(image, caption='Uploaded Image', use_column_width=True)

    # If the file is a PDF, display a message (you can implement further handling if needed)
    elif uploaded_file.type == "application/pdf":
        st.write("Uploaded PDF file.")

    # Ensure the temporary file is deleted after use
    os.remove(temp_file_path)
    st.write(f"Temporary file {temp_file_path} removed.")