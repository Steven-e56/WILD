from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import gradio as gr


# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
#old training dataset
model = BlipForConditionalGeneration.from_pretrained("./blip_finetuned_output")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
#specific csv dataset that we are training our blip model on.

def generate_caption(img):
    # Convert the numpy array image from Gradio to a PIL Image
    pil_image = Image.fromarray(img)

    # Prepare image for the model
    # The 'return_tensors="pt"' argument ensures the output is PyTorch tensors
    inputs = processor(images=pil_image, return_tensors="pt")

    # Generate the caption
    # The 'generate' method of the model creates the caption
    outputs = model.generate(**inputs)

    # Decode the generated tokens to a human-readable string
    # skip_special_tokens removes any special tokens like [CLS], [SEP]
    caption = processor.decode(outputs[0], skip_special_tokens=True)

    return caption

# Set up the Gradio interface
demo = gr.Interface(
    fn=generate_caption,
    inputs=[gr.Image(type="numpy", label="Upload your Image")], # Ensure input type is numpy for Image.fromarray
    outputs=[gr.Text(label="Generated Caption")],
    title="BLIP Image Captioning Demo",
    description="Upload an image and let the BLIP model generate a descriptive caption."
)

# Launch the Gradio app
demo.launch()          

#
