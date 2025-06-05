<<<<<<< HEAD
import gradio as gr
import base64
import requests
import json
import os

# Function to encode the image to base64
def encode_image(image_path):
    """Encodes an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        # Corrected: base64 instead of base66
        return base64.b64encode(image_file.read()).decode('utf-8')

# Asynchronous function to interact with the Gemini API
async def gemini_chat(image_path, text_input, chat_history):
    """
    Interacts with the Gemini 2.0 Flash model to generate a chatbot response,
    including image understanding.
    """
    # Placeholder for the API key in the Canvas environment
    # In a real deployment, you would secure this key.
    api_key = "" # If you want to use models other than gemini-2.0-flash or imagen-3.0-generate-002, provide an API key here. Otherwise, leave this as-is.
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Initialize chat history if empty
    if chat_history is None:
        chat_history = []

    # Prepare chat history for the API request
    formatted_chat_history = []
    for user_msg, model_msg in chat_history:
        if user_msg:
            formatted_chat_history.append({"role": "user", "parts": [{"text": user_msg}]})
        if model_msg:
            formatted_chat_history.append({"role": "model", "parts": [{"text": model_msg}]})

    # Add current user input and image (if provided)
    current_parts = [{"text": text_input}]
    if image_path:
        base64_image = encode_image(image_path)
        current_parts.append({
            "inlineData": {
                "mimeType": "image/jpeg", # Assuming JPEG, but could be dynamic based on image_path extension
                "data": base64_image
            }
        })
    formatted_chat_history.append({"role": "user", "parts": current_parts})

    payload = {
        "contents": formatted_chat_history
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts"):
            model_response = result["candidates"][0]["content"]["parts"][0]["text"]
            # Append the latest interaction to the chat history
            chat_history.append((text_input, model_response))
            return chat_history, "" # Return updated history and clear text input
        else:
            # More specific error message if content is missing
            return chat_history, "Error: Model response incomplete or invalid."

    except requests.exceptions.RequestException as e:
        return chat_history, f"Error calling Gemini API: {e}"
    except json.JSONDecodeError:
        return chat_history, "Error: Could not decode JSON response from API."
    except Exception as e:
        return chat_history, f"An unexpected error occurred: {e}"

# Define the Gradio interface
# Apply a theme here
with gr.Blocks(theme=gr.themes.Soft(), css="footer {visibility: hidden}") as demo:
    gr.Markdown(
        """
        # D.O.C Chatbot 
        **Ask me anything or describe the image.**
        ---
        """
    )

    with gr.Row():
        with gr.Column(scale=1): # Adjust column scale for better visual balance
            image_input = gr.Image(type="filepath", label="Upload or Drag and Drop Image Here", height=300)
            clear_button = gr.Button("Clear Chat and Image", variant="secondary") # Add an emoji and change variant

        with gr.Column(scale=2): # Give more space to the chatbot
            chatbot = gr.Chatbot(label="Conversation History", height=400, show_copy_button=True) # Add copy button
            text_input = gr.Textbox(placeholder="Type your message here...", label="Your Message", lines=2) # Increase lines
            submit_button = gr.Button("Send Message", variant="primary") # Add an emoji and change variant

    # Clear button functionality
    clear_button.click(
        lambda: (None, None, ""), # Clear image, chatbot, and text input
        outputs=[image_input, chatbot, text_input]
    )

    # Submit button functionality
    submit_button.click(
        gemini_chat,
        inputs=[image_input, text_input, chatbot],
        outputs=[chatbot, text_input],
        queue=False
    )

    # Allow pressing Enter to submit
    text_input.submit(
        gemini_chat,
        inputs=[image_input, text_input, chatbot],
        outputs=[chatbot, text_input],
        queue=False
    )

# Launch the Gradio app without share=True for local access
=======
import gradio as gr
import base64
import requests
import json
import os

# Function to encode the image to base64
def encode_image(image_path):
    """Encodes an image to a base64 string."""
    with open(image_path, "rb") as image_file:
        # Corrected: base64 instead of base66
        return base64.b64encode(image_file.read()).decode('utf-8')

# Asynchronous function to interact with the Gemini API
async def gemini_chat(image_path, text_input, chat_history):
    """
    Interacts with the Gemini 2.0 Flash model to generate a chatbot response,
    including image understanding.
    """
    # Placeholder for the API key in the Canvas environment
    # In a real deployment, you would secure this key.
    api_key = "" # If you want to use models other than gemini-2.0-flash or imagen-3.0-generate-002, provide an API key here. Otherwise, leave this as-is.
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Initialize chat history if empty
    if chat_history is None:
        chat_history = []

    # Prepare chat history for the API request
    formatted_chat_history = []
    for user_msg, model_msg in chat_history:
        if user_msg:
            formatted_chat_history.append({"role": "user", "parts": [{"text": user_msg}]})
        if model_msg:
            formatted_chat_history.append({"role": "model", "parts": [{"text": model_msg}]})

    # Add current user input and image (if provided)
    current_parts = [{"text": text_input}]
    if image_path:
        base64_image = encode_image(image_path)
        current_parts.append({
            "inlineData": {
                "mimeType": "image/jpeg", # Assuming JPEG, but could be dynamic based on image_path extension
                "data": base64_image
            }
        })
    formatted_chat_history.append({"role": "user", "parts": current_parts})

    payload = {
        "contents": formatted_chat_history
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts"):
            model_response = result["candidates"][0]["content"]["parts"][0]["text"]
            # Append the latest interaction to the chat history
            chat_history.append((text_input, model_response))
            return chat_history, "" # Return updated history and clear text input
        else:
            # More specific error message if content is missing
            return chat_history, "Error: Model response incomplete or invalid."

    except requests.exceptions.RequestException as e:
        return chat_history, f"Error calling Gemini API: {e}"
    except json.JSONDecodeError:
        return chat_history, "Error: Could not decode JSON response from API."
    except Exception as e:
        return chat_history, f"An unexpected error occurred: {e}"

# Define the Gradio interface
# Apply a theme here
with gr.Blocks(theme=gr.themes.Soft(), css="footer {visibility: hidden}") as demo:
    gr.Markdown(
        """
        # D.O.C Chatbot 
        **Ask me anything or describe the image.**
        ---
        """
    )

    with gr.Row():
        with gr.Column(scale=1): # Adjust column scale for better visual balance
            image_input = gr.Image(type="filepath", label="Upload or Drag and Drop Image Here", height=300)
            clear_button = gr.Button("Clear Chat and Image", variant="secondary") # Add an emoji and change variant

        with gr.Column(scale=2): # Give more space to the chatbot
            chatbot = gr.Chatbot(label="Conversation History", height=400, show_copy_button=True) # Add copy button
            text_input = gr.Textbox(placeholder="Type your message here...", label="Your Message", lines=2) # Increase lines
            submit_button = gr.Button("Send Message", variant="primary") # Add an emoji and change variant

    # Clear button functionality
    clear_button.click(
        lambda: (None, None, ""), # Clear image, chatbot, and text input
        outputs=[image_input, chatbot, text_input]
    )

    # Submit button functionality
    submit_button.click(
        gemini_chat,
        inputs=[image_input, text_input, chatbot],
        outputs=[chatbot, text_input],
        queue=False
    )

    # Allow pressing Enter to submit
    text_input.submit(
        gemini_chat,
        inputs=[image_input, text_input, chatbot],
        outputs=[chatbot, text_input],
        queue=False
    )

# Launch the Gradio app without share=True for local access
>>>>>>> bf28cc251c3fb1bb98f393412ea716975fe06449
demo.launch()