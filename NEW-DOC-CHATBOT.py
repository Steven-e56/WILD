import gradio as gr
import base64
import requests
import json
import os

# Function to encode the image to base64 (still relevant if your local LLM supports vision)
def encode_image(image_path):
    """Encodes an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to interact with the local LLM via Ollama
async def local_llm_chat(image_path, text_input, chat_history):
    """
    Interacts with a local LLM running via Ollama to generate a chatbot response,
    including image understanding if the local model supports it (e.g., LLaVA).
    """
    # Ollama API endpoint (default local address)
    ollama_api_url = "http://localhost:11434/api/chat"
    # Choose the model you have downloaded and want to use.
    # Examples: "llama3.1", "llava" (for multimodal), "mistral", "gemma"
    model_name = "llama3.1" # <--- IMPORTANT: Change this to the model you pulled with Ollama

    # Initialize chat history if empty
    if chat_history is None:
        chat_history = []

    # Prepare messages for Ollama's chat API
    # Ollama's API expects a list of messages with 'role' and 'content'
    messages = []
    for user_msg, model_msg in chat_history:
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})

    # Add current user input and image (if provided)
    current_content = [{"type": "text", "text": text_input}]
    if image_path:
        base64_image = encode_image(image_path)
        # Ollama's vision models (like LLaVA) expect image data in a specific format
        current_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})

    messages.append({"role": "user", "content": current_content})

    payload = {
        "model": model_name,
        "messages": messages,
        "stream": False # Set to True for streaming responses (requires different handling)
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ollama_api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()

        if result.get("message") and result["message"].get("content"):
            model_response = result["message"]["content"]
            # Append the latest interaction to the chat history
            chat_history.append((text_input, model_response))
            return chat_history, "" # Return updated history and clear text input
        else:
            return chat_history, "Error: Local LLM response incomplete or invalid."

    except requests.exceptions.RequestException as e:
        return chat_history, f"Error calling local LLM via Ollama: {e}. Make sure Ollama is running and the model '{model_name}' is pulled."
    except json.JSONDecodeError:
        return chat_history, "Error: Could not decode JSON response from local LLM."
    except Exception as e:
        return chat_history, f"An unexpected error occurred: {e}"

# Define the Gradio interface (mostly the same as your original, but using the new function)
with gr.Blocks(theme=gr.themes.Soft(), css="footer {visibility: hidden}") as demo:
    gr.Markdown(
        """
        # D.O.C Chatbot (Local LLM)
        **Ask me anything or describe the image.**
        ---
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="filepath", label="Upload or Drag and Drop Image Here", height=300)
            clear_button = gr.Button("Clear Chat and Image", variant="secondary")

        with gr.Column(scale=2):
            chatbot = gr.Chatbot(label="Conversation History", height=400, show_copy_button=True)
            text_input = gr.Textbox(placeholder="Type your message here...", label="Your Message", lines=2)
            submit_button = gr.Button("Send Message", variant="primary")

    clear_button.click(
        lambda: (None, None, ""),
        outputs=[image_input, chatbot, text_input]
    )

    submit_button.click(
        local_llm_chat, # Use the new local LLM function
        inputs=[image_input, text_input, chatbot],
        outputs=[chatbot, text_input],
        queue=False
    )

    text_input.submit(
        local_llm_chat, # Use the new local LLM function
        inputs=[image_input, text_input, chatbot],
        outputs=[chatbot, text_input],
        queue=False
    )

demo.launch(share=True)