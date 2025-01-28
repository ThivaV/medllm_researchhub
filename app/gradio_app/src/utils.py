import base64


def is_image(file_path):
    """Check valid for image file extensions"""
    image_extensions = [
        ".jpeg",
        ".jpg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".svg",
        ".pdf",
    ]
    return any(file_path.lower().endswith(ext) for ext in image_extensions)


def encode_image(image_path):
    """Function to encode the image"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def construct_conversation_history(chat_history):
    """Build conversation history"""
    messages = []
    previous_role = None
    combined_content = []

    for history in chat_history:
        role = history["role"]
        content = history["content"]

        if isinstance(content, tuple) and len(content) > 0:
            content = content[0]

        if role == "user":
            if isinstance(content, str) and is_image(content):
                base64_file = encode_image(content)
                part = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_file}"},
                }
            else:
                part = {"type": "text", "text": content}

            if role == previous_role:
                combined_content.append(part)
            else:
                # Only append previous combined content if previous role was user
                if previous_role == "user" and combined_content:
                    messages.append(
                        {"role": previous_role, "content": combined_content}
                    )
                combined_content = [part]
        else:
            # Handle non-user role
            if previous_role == "user" and combined_content:
                messages.append({"role": "user", "content": combined_content})
                combined_content = []
            messages.append({"role": role, "content": content})

        previous_role = role

    # Add any remaining combined content after loop ends
    if combined_content:
        messages.append({"role": previous_role, "content": combined_content})

    return messages


def construct_latest_conversation(latest_message, messages):
    """Build latest conversation-
    # Add new user message
    # Extract the text and files"""
    text = latest_message["text"]
    files = latest_message["files"]

    input_messages = []
    if len(files) > 0:
        for file in files:
            base64_file = encode_image(file)
            input_messages.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_file}"},
                }
            )

        input_messages.append({"type": "text", "text": text})
        messages.append({"role": "user", "content": input_messages})
    else:
        messages.append({"role": "user", "content": text})

    return messages
