import streamlit as st

from src.utils import upload_files, initialize_retriever
from src.groq_ops import chat


def initialize():
    """BioMED ⚕️ VisionLM AI Tool initialization"""
    st.title("BioMEDICAL VisionLM AI Tool")
    st.info(
        "🚨 This application is designed as a comprehensive AI tool for medical analysis, leveraging advanced multimodal capabilities to assist healthcare professionals and potentially extend access to underserved communities."
    )

    # Initialize session states for api keys
    if "groq_apikey" not in st.session_state:
        st.session_state.groq_apikey = None

    if "hf_apikey" not in st.session_state:
        st.session_state.hf_apikey = None

    col1, col2 = st.columns([1, 3], vertical_alignment="top", border=False)

    with col1:
        st.session_state.groq_apikey = st.text_input(
            "Enter your GROQ API key 👇", type="password"
        )
        st.session_state.hf_apikey = st.text_input(
            "Enter your HuggingFace API key 👇", type="password"
        )

        files = upload_files()
        report_summary, retriever = initialize_retriever(files, k=5)

    with col2:
        msg = st.container(height=800, border=True)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

            # Append uploaded reports summary to the session history
            # to display in the chat window
            st.session_state.messages.append(
                {"role": "assistant", "content": report_summary}
            )

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with msg.chat_message(message["role"]):
                st.markdown(message["content"])

        if query := st.chat_input("Say something"):
            # Display user message in chat message container
            with msg.chat_message("user"):
                st.write(query)
                st.session_state.messages.append({"role": "user", "content": query})

            # Retrieve relavant documents
            docs = retriever.invoke(query)

            # Display assistant response in chat message container
            with msg.chat_message("assistant"):
                response = talk_to_bot(query, docs)
                st.write(response)

                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )


def talk_to_bot(query, documents) -> str:
    """talking to bot"""

    context_parts = [doc.page_content for doc in documents]
    context = "\n\n".join(context_parts)

    prompt_template = """
    System Instruction: You are a helpful AI assistant capable of understanding bio medical informations. 
    Use the provided chat history, context, and user query to generate a relevant and accurate response.

    Chat History: {chat_history}

    Context: {context}

    User Query: {query}
    """

    chat_history = st.session_state.messages
    prompt = prompt_template.format(
        chat_history=chat_history, context=context, query=query
    )

    message = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

    response = chat(message)
    return response
