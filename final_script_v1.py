import os
import time
import threading
import numpy as np
from PIL import Image
import piexif
import cv2
from ultralytics import YOLO
from transformers import BlipProcessor, BlipForConditionalGeneration
from gpt4all import GPT4All
import gradio as gr  # Keep this for later UI

# === Config ===
INPUT_FOLDER = "saved_frames"
PROCESSED_FOLDER = os.path.join(INPUT_FOLDER, "processed")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# YOLO model and video source (webcam 0 or path)
YOLO_MODEL_PATH = "C:/Users/m272514/Desktop/roboflow_dataset_v2/runs/detect/train/weights/best.pt"
VIDEO_SOURCE = 0

# LLaMA model config
LLAMA_MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
LLAMA_MODEL_PATH = r"C:\Users\zachary.daher\AppData\Local\nomic.ai\GPT4All"

# === Initialize models ===

print("[INFO] Loading YOLO model...")
yolo_model = YOLO(YOLO_MODEL_PATH)

print("[INFO] Loading BLIP model...")
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

print("[INFO] Loading LLaMA model...")
llama_model = GPT4All(LLAMA_MODEL_NAME, model_path=LLAMA_MODEL_PATH)
llama_model.open()
print("[INFO] Models loaded and ready.")

# === Helpers ===

def generate_caption_from_pil(pil_image):
    inputs = blip_processor(images=pil_image, return_tensors="pt")
    outputs = blip_model.generate(**inputs)
    caption = blip_processor.decode(outputs[0], skip_special_tokens=True)
    return caption

def classify_triage_level(caption):
    prompt = f"""
You are a triage assistant. Based on the description of a person from an image, return a single triage level from 1 to 5:

1 = Critical (requires immediate attention)
2 = Serious
3 = Moderate
4 = Minor
5 = Deceased

ONLY return the number, no explanation.

Caption: "{caption}"
Triage level:
"""
    response = llama_model.generate(prompt=prompt, max_tokens=5).strip()
    try:
        level = int(response[0])
        if level in [1, 2, 3, 4, 5]:
            return level
    except Exception:
        pass
    return 3  # fallback moderate

def embed_caption_and_triage(image_path, caption, triage_level):
    img = Image.open(image_path)
    try:
        exif_dict = piexif.load(img.info.get("exif", b""))
    except Exception:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    # Embed caption in ImageDescription
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = caption.encode("utf-8")

    # Embed triage level in UserComment (ASCII with prefix)
    prefix = b"ASCII\x00\x00\x00"
    triage_str = f"Triage Level: {triage_level}"
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = prefix + triage_str.encode("ascii")

    exif_bytes = piexif.dump(exif_dict)
    img.save(image_path, exif=exif_bytes)

# === Frame saving from video with YOLO + DeepSORT ===
seen_ids = set()
frame_id = 0

cap = cv2.VideoCapture(VIDEO_SOURCE)

def process_frame(frame):
    global seen_ids
    results = yolo_model.track(frame, persist=True, tracker="deep_sort.yaml", verbose=False)
    boxes = results[0].boxes
    saved = False

    if boxes.id is not None:
        for i in range(len(boxes.id)):
            track_id = int(boxes.id[i])
            class_id = int(boxes.cls[i])

            if yolo_model.names[class_id] == 'person' and track_id not in seen_ids:
                seen_ids.add(track_id)
                save_path = os.path.join(INPUT_FOLDER, f'person_{track_id:06d}.jpeg')
                cv2.imwrite(save_path, frame)
                print(f"Saved frame for person {track_id} at frame {frame_id}")
                saved = True
    return saved

# === Watch folder for new images, caption + triage + embed metadata ===
def process_saved_images():
    while True:
        try:
            for filename in os.listdir(INPUT_FOLDER):
                if not filename.lower().endswith(".jpeg"):
                    continue
                path = os.path.join(INPUT_FOLDER, filename)

                # Only process if not already moved to processed folder
                if os.path.exists(os.path.join(PROCESSED_FOLDER, filename)):
                    continue

                pil_img = Image.open(path).convert("RGB")

                # Generate caption
                caption = generate_caption_from_pil(pil_img)
                print(f"[CAPTION] {filename} → {caption}")

                # Classify triage
                triage_level = classify_triage_level(caption)
                print(f"[TRIAGE] {filename} → Level {triage_level}")

                # Embed metadata
                embed_caption_and_triage(path, caption, triage_level)

                # Move to processed folder
                os.rename(path, os.path.join(PROCESSED_FOLDER, filename))
                print(f"[DONE] Processed and moved {filename}")

        except Exception as e:
            print(f"[ERROR] Folder processing error: {e}")

        time.sleep(2)  # check every 2 sec

# === Start background thread to process saved images ===
import threading
threading.Thread(target=process_saved_images, daemon=True).start()

# === Main video capture loop ===
print("[INFO] Starting video capture and detection... Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] Video capture ended.")
        break

    process_frame(frame)
    frame_id += 1

    cv2.imshow("YOLO Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
llama_model.close()
print("[INFO] Program ended.")

# === Gradio interface for manual testing ===
def gradio_caption_and_triage(pil_image):
    caption = generate_caption_from_pil(pil_image)
    triage_level = classify_triage_level(caption)
    return caption, f"Triage Level: {triage_level}"

demo = gr.Interface(
    fn=gradio_caption_and_triage,
    inputs=gr.Image(type="pil"),
    outputs=[gr.Textbox(label="BLIP Caption"), gr.Textbox(label="Triage Level")],
    title="BLIP + LLaMA Triage Demo",
    description="Upload an image to get the BLIP caption and triage level."
)

# To launch the Gradio UI later, uncomment the next line:
# demo.launch()
