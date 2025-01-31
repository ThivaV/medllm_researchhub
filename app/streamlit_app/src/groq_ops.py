import streamlit as st
from groq import Groq


def chat(message: str) -> str:
    """Chatbot response generator"""

    client = Groq(api_key=st.session_state.groq_apikey)

    completion = client.chat.completions.create(
        messages=message,
        model="llama-3.2-90b-vision-preview",
        # max_completion_tokens=1024,
        # temperature=0.5,
        # top_p=1,
        # stop=None,
        stream=False,
    )

    response = completion.choices[0].message.content
    return response
