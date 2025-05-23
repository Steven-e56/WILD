from datasets import load_dataset, Features, Value, Image as HFImage

# Step 1: Load your CSV
dataset = load_dataset("csv", data_files="fine_tune_dataset.csv")["train"]

# Step 2: Tell Hugging Face that the "image" column points to image files
dataset = dataset.cast(
    Features({
        "image": HFImage(),          # Actually load image data (as PIL)
        "caption": Value("string")   # Keep captions as text
    })
)

# Step 3: Test it
print(dataset[0])
dataset[0]["image"].show()  # This should display an image
