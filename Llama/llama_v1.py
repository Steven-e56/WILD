import os
from PIL import Image
import piexif
from gpt4all import GPT4All

# === Configuration ===
INPUT_FOLDER = "saved_frames/processed"
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model_path = r"C:\Users\zachary.daher\AppData\Local\nomic.ai\GPT4All"

# === Load LLaMA once ===
print("[INFO] Loading LLaMA model...")
llama_model = GPT4All(model_name, model_path=model_path)
llama_model.open()
print("[INFO] Model loaded and ready.")

# === Helper: Read caption from ImageDescription ===
def read_caption(image_path):
    exif_dict = piexif.load(image_path)
    caption_bytes = exif_dict["0th"].get(piexif.ImageIFD.ImageDescription, b"")
    if caption_bytes:
        return caption_bytes.decode("utf-8")
    return ""

# === Helper: Check if triage already embedded ===
def has_triage_tag(image_path):
    try:
        exif = piexif.load(image_path)
        user_comment = exif["Exif"].get(piexif.ExifIFD.UserComment, b"")
        return b"Triage Level" in user_comment
    except Exception:
        return False

# === Helper: Generate triage level from caption ===
def classify_triage_level(caption):
    prompt = f"""
You are a triage assistant. Based on the description of a person from an image, return a single triage level from 1 to 5:

1 = Critical (requires immediate attention)  
2 = Serious  
3 = Moderate  
4 = Minor  
5 = Uninjured

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
    # fallback if parsing fails
    return 3

# === Helper: Embed caption and triage separately ===
def embed_caption_and_triage(image_path, caption, triage_level):
    img = Image.open(image_path)
    exif_dict = piexif.load(img.info.get("exif", b""))

    # Set caption in ImageDescription (UTF-8)
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = caption.encode("utf-8")

    # Set triage level in UserComment (ASCII with prefix)
    prefix = b"ASCII\x00\x00\x00"
    triage_str = f"Triage Level: {triage_level}"
    exif_dict["Exif"][piexif.ExifIFD.UserComment] = prefix + triage_str.encode("ascii")

    exif_bytes = piexif.dump(exif_dict)
    img.save(image_path, exif=exif_bytes)

# === Main loop ===
print("[INFO] Processing images for triage classification...")
for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith(".jpeg"):
        continue

    path = os.path.join(INPUT_FOLDER, filename)

    try:
        if has_triage_tag(path):
            print(f"[SKIP] {filename} already has triage level.")
            continue

        caption = read_caption(path)
        if not caption:
            print(f"[WARN] No caption found in {filename}, skipping.")
            continue

        triage_level = classify_triage_level(caption)
        embed_caption_and_triage(path, caption, triage_level)
        print(f"[OK] {filename} → Triage Level {triage_level}")

    except Exception as e:
        print(f"[ERROR] Failed on {filename}: {e}")

# Cleanup
llama_model.close()
print("[DONE] All images processed.")
