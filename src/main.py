import streamlit as st  # type: ignore
import random
import time
# import tempfile
# from PIL import Image

from src.helper import upload_files

def initialize():
    """BioMED ⚕️ VisionLM AI Tool initialization"""
    st.title("BioMEDICAL VisionLM AI Tool")
    st.info(
        "🚨 This application is designed as a comprehensive AI tool for medical analysis, leveraging advanced multimodal capabilities to assist healthcare professionals and potentially extend access to underserved communities."
    )

    col1, col2 = st.columns([1, 3], vertical_alignment="top", border=False)

    with col1:
        reports = upload_files()
        st.write("Uploaded files: ", reports)

    with col2:
        msg = st.container(height=800, border=True)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with msg.chat_message(message["role"]):
                msg.markdown(message["content"])

        query = st.chat_input("Say something")
        if query:
            # Display user message in chat message container
            with msg.chat_message("user"):
                msg.markdown(query)

            # Display assistant response in chat message container
            with msg.chat_message("assistant"):
                response = msg.write_stream(response_generator())

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )

    for word in response.split():
        yield word + " "
        time.sleep(0.05)