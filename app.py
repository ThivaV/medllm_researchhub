# import base64
# import gradio as gr
# from groq import Groq


# def is_image_or_pdf(file_path):
#     image_extensions = [
#         ".jpeg",
#         ".jpg",
#         ".png",
#         ".gif",
#         ".bmp",
#         ".tiff",
#         ".svg",
#         ".pdf",
#     ]
#     return any(file_path.endswith(ext) for ext in image_extensions)


# # Function to encode the image
# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")


# def chat(message, chat_history, api_key):
#     if not api_key.strip():
#         return "⚠️ Please enter your GROQ API key first!"

#     try:
#         print("\nmessage: ", message)
#         print("\nchat_history: ", chat_history)

#         client = Groq(api_key=api_key.strip())

#         # Build conversation history
#         messages = []
#         for history in chat_history:
#             content = history["content"]
#             if isinstance(content, tuple) and len(content) > 0:
#                 content = content[0]

#             msg = ""
#             if isinstance(content, str) and is_image_or_pdf(content):
#                 print("Image URL found:", content)
#                 base64_file = encode_image(content)
#                 msg = {
#                     "type": "image_url",
#                     "image_url": {"url": f"data:image/jpeg;base64,{base64_file}"},
#                 }
#             else:
#                 msg = history["content"]

#             messages.append({"role": history["role"], "content": msg})

#         # Add new user message
#         # Extract the text and files
#         text = message["text"]
#         files = message["files"]

#         input_messages = []
#         if len(files) > 0:
#             for file in files:
#                 base64_file = encode_image(file)
#                 input_messages.append(
#                     {
#                         "type": "image_url",
#                         "image_url": {"url": f"data:image/jpeg;base64,{base64_file}"},
#                     }
#                 )
        
#             input_messages.append({"type": "text", "text": text})
#             messages.append({"role": "user", "content": input_messages})
#         else:
#             messages.append({"role": "user", "content": text})

#         print("\nchat_history+message: ", messages)

#         chat_completion = client.chat.completions.create(
#             messages=messages,
#             model="llama-3.2-90b-vision-preview",
#             temperature=0.7,
#             max_tokens=1024,
#         )

#         bot_message = chat_completion.choices[0].message.content
#         return bot_message
#     except Exception as e:
#         return f"❌ Error: {str(e)}"


# with gr.Blocks() as demo:
#     with gr.Accordion("Enter your Groq key!", open=False):
#         api_key = gr.Textbox(
#             label="GROQ API Key", placeholder="Enter your key here...", type="password"
#         )

#     with gr.Accordion("BioMEDICAL VisionLM AI Tool", open=True):
#         gr.ChatInterface(
#             title="BioMED⚕️",
#             description="> 🚨 This application is designed as a comprehensive AI tool for medical analysis, leveraging advanced multimodal capabilities to assist healthcare professionals and potentially extend access to underserved communities.",
#             theme="gradio/monochrome",
#             show_progress="full",
#             fill_height=True,
#             fill_width=True,
#             fn=chat,
#             additional_inputs=api_key,
#             type="messages",
#             multimodal=True,
#             examples=[],
#         )

# if __name__ == "__main__":
#     demo.launch(share=True)

import base64
import gradio as gr
from groq import Groq

def is_image_or_pdf(file_path):
    image_extensions = [".jpeg", ".jpg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".pdf"]
    return any(file_path.endswith(ext) for ext in image_extensions)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def chat(message, chat_history, api_key):
    if not api_key.strip():
        return "⚠️ Please enter your GROQ API key first!"

    try:
        client = Groq(api_key=api_key.strip())
        messages = []

        # Process chat history
        for history in chat_history:
            content = history["content"]
            role = history["role"]
            
            if isinstance(content, str) and is_image_or_pdf(content):
                # Handle image from history
                base64_file = encode_image(content)
                messages.append({
                    "role": role,
                    "content": [{
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_file}"}
                    }]
                })
            else:
                # Handle text or existing structured content
                messages.append({"role": role, "content": content})

        # Process new message
        text = message["text"]
        files = message["files"]
        new_content = []

        if files:
            for file in files:
                base64_file = encode_image(file)
                new_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_file}"}
                })
            new_content.append({"type": "text", "text": text})
        else:
            new_content = text

        messages.append({"role": "user", "content": new_content})

        # API call
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.2-90b-vision-preview",
            temperature=0.7,
            max_tokens=1024
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"

with gr.Blocks() as demo:
    with gr.Accordion("Enter your Groq key!", open=False):
        api_key = gr.Textbox(label="GROQ API Key", placeholder="Enter your key here...", type="password")
    
    with gr.Accordion("BioMEDICAL VisionLM AI Tool", open=True):
        gr.ChatInterface(
            fn=chat,
            additional_inputs=api_key,
            multimodal=True,
            title="BioMED⚕️",
            description="Advanced medical analysis AI tool with multimodal capabilities"
        )

if __name__ == "__main__":
    demo.launch(share=True)