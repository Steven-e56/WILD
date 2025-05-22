from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os

def caption_images_in_folder(folder_path):
    """
    Reads through a specified folder, captions each image found,
    and returns a dictionary of image filenames and their captions.

    Args:
        folder_path (str): The path to the folder containing images.

    Returns:
        dict: A dictionary where keys are image filenames and values are their captions.
              Returns an empty dictionary if the folder is not found or contains no images.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found at '{folder_path}'")
        return {}

    # Initialize processor and model globally (or here if this function is called once)
    # This ensures they are loaded only once, which is efficient.
    print("Loading BLIP processor and model... This may take a moment.")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    print("Model loaded successfully.")

    image_captions = {}
    supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')

    print(f"\nScanning folder: '{folder_path}' for images...")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(supported_extensions):
            image_path = os.path.join(folder_path, filename)
            try:
                # Open the image
                img_pil = Image.open(image_path).convert("RGB") # Convert to RGB to handle all image modes

                # Prepare image for the model
                inputs = processor(images=img_pil, return_tensors="pt")

                # Generate the caption
                outputs = model.generate(**inputs)

                # Decode the generated tokens
                caption = processor.decode(outputs[0], skip_special_tokens=True)

                image_captions[filename] = caption
                print(f"  - Processed '{filename}': {caption}")

            except Exception as e:
                print(f"  - Error processing '{filename}': {e}")
        else:
            print(f"  - Skipping non-image file: '{filename}'")

    if not image_captions:
        print("No supported images found in the folder.")

    return image_captions

# --- Main execution part ---
if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your folder containing images
    # Example:
    # my_image_folder = "C:\\Users\\m270318\\MyImages"
    # my_image_folder = "/mnt/c/Users/m270318/MyImages" # For WSL users accessing Windows path
    # my_image_folder = "./test_images" # If you have a folder named 'test_images' in the same directory as this script

    # For demonstration, let's create a dummy folder and some dummy images if they don't exist
    dummy_folder = "temp_blip_images"
    os.makedirs(dummy_folder, exist_ok=True)

    # Create dummy image files if they don't exist
    try:
        from PIL import ImageDraw, ImageFont
        # Create a simple white image with text
        img1 = Image.new('RGB', (200, 100), color = (255, 255, 255))
        d = ImageDraw.Draw(img1)
        # Try to load a default font or use a basic one
        try:
            fnt = ImageFont.truetype("arial.ttf", 20) # Common font on Windows
        except IOError:
            fnt = ImageFont.load_default()
        d.text((10,10), "Hello World!", fill=(0,0,0), font=fnt)
        img1.save(os.path.join(dummy_folder, 'dummy_image_1.png'))

        img2 = Image.new('RGB', (200, 100), color = (0, 0, 255))
        d = ImageDraw.Draw(img2)
        d.text((10,10), "Blue Square", fill=(255,255,255), font=fnt)
        img2.save(os.path.join(dummy_folder, 'dummy_image_2.jpg'))

        print(f"Created dummy images in '{dummy_folder}' for demonstration.")
        my_image_folder = dummy_folder

    except ImportError:
        print("Pillow ImageDraw/ImageFont not available. Please ensure Pillow is fully installed for dummy image creation.")
        print(f"Please manually create some images in the '{dummy_folder}' folder or update 'my_image_folder' variable.")
        my_image_folder = dummy_folder # Still point to the dummy folder, hoping user puts images there

    # Call the function to caption images
    captions = caption_images_in_folder(my_image_folder)

    print("\n--- All Captions ---")
    if captions:
        for filename, caption in captions.items():
            print(f"'{filename}': {caption}")
    else:
        print("No captions generated.")