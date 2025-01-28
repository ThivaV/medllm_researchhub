import gradio as gr
from groq import Groq

from src.utils import construct_conversation_history, construct_latest_conversation


def chat(message, chat_history, api_key):
    if not api_key.strip():
        return "⚠️ Please enter your GROQ API key first!"

    try:
        client = Groq(api_key=api_key.strip())

        # Build conversation history
        messages = construct_conversation_history(chat_history)

        # Build latest conversation
        messages = construct_latest_conversation(message, messages)

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.2-90b-vision-preview",
            temperature=0.7,
            max_tokens=1024,
        )

        bot_message = chat_completion.choices[0].message.content
        return bot_message
    except Exception as e:
        return f"❌ Error: {str(e)}"


if __name__ == "__main__":
    with gr.Blocks() as app:
        with gr.Accordion("Enter your Groq key!", open=False):
            api_key = gr.Textbox(
                label="GROQ API Key",
                placeholder="Enter your key here...",
                type="password",
            )

        with gr.Accordion("BioMEDICAL VisionLM AI Tool", open=True):
            gr.ChatInterface(
                title="BioMED⚕️",
                description="> 🚨 This application is designed as a comprehensive AI tool for medical analysis, leveraging advanced multimodal capabilities to assist healthcare professionals and potentially extend access to underserved communities.",
                theme="soft",
                show_progress="full",
                fill_height=True,
                fill_width=True,
                fn=chat,
                additional_inputs=api_key,
                type="messages",
                multimodal=True,
                save_history=True,
                examples=[],
            )

    app.launch(share=True)
