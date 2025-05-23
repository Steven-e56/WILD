import os
import csv

# Folder that contains your image folders
base_dir = r"C:\APL_WILD\WILD\LLM_LLAMA\blip_training_code"

# Output CSV file path
output_csv = os.path.join(base_dir, "fine_tune_dataset.csv")

# Create the CSV file
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["image", "caption"])  # Header

    # Loop through each folder
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)

        if not os.path.isdir(folder_path):
            continue  # Skip files

        for img in os.listdir(folder_path):
            if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                relative_path = f"{folder}/{img}"
                writer.writerow([relative_path, ""])  # Leave caption blank
