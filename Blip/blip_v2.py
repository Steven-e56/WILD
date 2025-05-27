import os
import time
import threading
from PIL import Image
import piexif
from transformers import BlipProcessor, BlipForConditionalGeneration
import gradio as gr

# Initialize BLIP
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Folder settings
INPUT_FOLDER = "saved_frames"
PROCESSED_FOLDER = os.path.join(INPUT_FOLDER, "processed")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Captioning function now accepts PIL Image directly
def generate_caption(pil_image):
    inputs = processor(images=pil_image, return_tensors="pt")
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption


def embed_description_in_image(image_path, description):
    img = Image.open(image_path)

    # Load or initialize EXIF data
    try:
        exif_dict = piexif.load(img.info.get("exif", b""))
    except Exception:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    # Add description (convert to bytes)
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode("utf-8")

    # Write back to image
    exif_bytes = piexif.dump(exif_dict)
    img.save(image_path, "jpeg", exif=exif_bytes)


# Helper to check if image already has a caption in EXIF
def has_caption(image_path):
    try:
        exif_dict = piexif.load(image_path)
        desc = exif_dict["0th"].get(piexif.ImageIFD.ImageDescription, b"")
        if desc and desc.strip():
            return True
    except Exception:
        pass
    return False


# Folder watcher (background)
def watch_folder():
    while True:
        for filename in os.listdir(INPUT_FOLDER):
            if not filename.lower().endswith(".jpeg"):
                continue
            path = os.path.join(INPUT_FOLDER, filename)

            # Skip if already moved to processed folder
            if os.path.exists(os.path.join(PROCESSED_FOLDER, filename)):
                continue

            # Skip if already has a caption
            if has_caption(path):
                continue

            try:
                pil_img = Image.open(path).convert("RGB")
                caption = generate_caption(pil_img)
                print(f"[AUTO] {filename} → {caption}")

                # Embed caption into the image
                embed_description_in_image(path, caption)

                # Move to processed folder to avoid re-processing
                os.rename(path, os.path.join(PROCESSED_FOLDER, filename))
            except Exception as e:
                print(f"[ERROR] {filename} → {e}")

        time.sleep(2)  # Check every 2 seconds


# Start folder watcher in background thread
threading.Thread(target=watch_folder, daemon=True).start()


# Launch Gradio interface
demo = gr.Interface(
    fn=generate_caption,
    inputs=[gr.Image(type="pil", label="Upload Image")],
    outputs=[gr.Text(label="Caption")],
    title="BLIP Captioning (with Folder Auto-Scan)",
    description="Upload or drop images below. Auto-scans saved_frames/ for captioning."
)
demo.launch()


# HOW TO READ METADATA LATER

# img = Image.open("processed/frame_001.jpeg")
# exif_data = piexif.load(img.info["exif"])
# description = exif_data["0th"][piexif.ImageIFD.ImageDescription].decode("utf-8")
# print("Description:", description)