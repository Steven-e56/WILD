import os
import time
import threading
import numpy as np
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import gradio as gr

# Initialize BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Folder settings
INPUT_FOLDER = "saved_frames"
PROCESSED_FOLDER = os.path.join(INPUT_FOLDER, "processed")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Captioning function (shared)
def generate_caption(img):
    pil_image = Image.fromarray(img)
    inputs = processor(images=pil_image, return_tensors="pt")
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

# Folder watcher (background)
def watch_folder():
    while True:
        for filename in os.listdir(INPUT_FOLDER):
            if not filename.endswith(".jpg"):
                continue
            path = os.path.join(INPUT_FOLDER, filename)
            try:
                pil_img = Image.open(path).convert("RGB")
                img_np = np.array(pil_img)
                caption = generate_caption(img_np)
                print(f"[AUTO] {filename} → {caption}")
                os.rename(path, os.path.join(PROCESSED_FOLDER, filename))
            except Exception as e:
                print(f"[ERROR] {filename} → {e}")
        time.sleep(2)  # Check every 2 sec

# Start folder watcher in background
threading.Thread(target=watch_folder, daemon=True).start()

# Launch Gradio interface
demo = gr.Interface(
    fn=generate_caption,
    inputs=[gr.Image(type="numpy", label="Upload Image")],
    outputs=[gr.Text(label="Caption")],
    title="BLIP Captioning (with Folder Auto-Scan)",
    description="Upload or drop images below. Auto-scans saved_frames/ for captioning."
)
demo.launch()