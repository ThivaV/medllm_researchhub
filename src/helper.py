import streamlit as st
# import tempfile
# from PIL import Image


def upload_files():
    """Upload files"""

    # File uploader for both images and PDFs
    uploaded_files = st.file_uploader(
        "Choose files...",
        type=["jpg", "png", "jpeg", "pdf"],
        accept_multiple_files=True,
    )

    return uploaded_files