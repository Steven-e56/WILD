import os
import time
import requests
from PIL import Image

# Settings
INPUT_FOLDER = "saved_frames"
PROCESSED_FOLDER = os.path.join(INPUT_FOLDER, "processed")
BLIP_URL = "http://localhost:5000/classify"  # Replace with your BLIP endpoint

# Ensure processed folder exists
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def send_image_to_blip(image_path):
    try:
        with open(image_path, "rb") as img_file:
            response = requests.post(
                BLIP_URL,
                files={"image": (os.path.basename(image_path), img_file, "image/jpeg")}
            )
        if response.status_code == 200:
            caption = response.json().get("caption", "No caption returned")
            print(f"[BLIP] {os.path.basename(image_path)} → {caption}")
        else:
            print(f"[ERROR] {image_path} → {response.status_code}")
    except Exception as e:
        print(f"[Exception] {image_path} → {str(e)}")

def process_images():
    while True:
        image_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".jpg")]
        for filename in image_files:
            image_path = os.path.join(INPUT_FOLDER, filename)
            try:
                # Verify image is fully saved
                with Image.open(image_path) as im:
                    im.verify()

                send_image_to_blip(image_path)

                # Move to processed folder
                os.rename(image_path, os.path.join(PROCESSED_FOLDER, filename))
            except Exception as e:
                print(f"[Skip] {filename} → {e}")
                continue
        time.sleep(1)  # Polling interval

if __name__ == "__main__":
    print("📤 Watching folder and sending images to BLIP...")
    process_images()
