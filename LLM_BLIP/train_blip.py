# from transformers import BlipProcessor, BlipForConditionalGeneration, Trainer, TrainingArguments
# from datasets import Dataset, load_dataset, Image
# import pandas as pd

# csv_path = "fine_tune_dataset_withoutcaptions(FILLED IN)- Copy.csv"
# #r"C:\Users\m260588\Box\Academy_Students\Team 3\fine_tune_dataset.csv"
# df = pd.read_csv(csv_path)
# dataset = Dataset.from_pandas(df)
# dataset = dataset.cast_column("image", Image())

# # === Step 2: Load BLIP processor and model ===
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# # === Step 3: Preprocessing ===


# def preprocess(example):
#     inputs = processor(images=example["image"], text=example["caption"],
#                     #padding="max_length", truncation=True, return_tensors="pt")
#     return {
#         "input_ids": inputs.input_ids[0],
#         "attention_mask": inputs.attention_mask[0],
#         "pixel_values": inputs.pixel_values[0],
#         "labels": inputs.input_ids[0],
#     }
# dataset = dataset.map(preprocess)

# # === Step 4: Training Arguments ===
# training_args = TrainingArguments(
#     output_dir="./blip_finetuned_output",
#     per_device_train_batch_size=2,
#     num_train_epochs=3,
#     logging_dir="./logs",
#     logging_steps=5,
#     save_steps=50,
#     save_total_limit=1,
#     remove_unused_columns=False
# )

# # === Step 5: Trainer ===
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=dataset,
#     tokenizer=processor,
# )

# # === Step 6: Train! ===
# trainer.train()
from transformers import BlipProcessor, BlipForConditionalGeneration, Trainer, TrainingArguments, default_data_collator
from datasets import Dataset, Image
import pandas as pd

# === Step 1: Load CSV as Hugging Face Dataset ===
csv_path = "fine_tune_dataset_cleaned.csv"
df = pd.read_csv(csv_path, encoding="utf-8")
dataset = Dataset.from_pandas(df)
dataset = dataset.cast_column("image", Image())

# === Step 2: Load BLIP processor and model ===
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model     = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# === Step 3: Preprocessing function ===
def preprocess(example):
    # ---- image-only ----
    pixel_values = processor(
        images=example["image"],
        return_tensors="pt"
    ).pixel_values[0]
    # ---- text-only ----
    text_inputs = processor.tokenizer(
        example["caption"],
        padding="max_length",
        truncation=True,
        max_length=processor.tokenizer.model_max_length,
        return_tensors="pt"
    )
    input_ids      = text_inputs.input_ids[0]
    attention_mask = text_inputs.attention_mask[0]
    labels         = input_ids.clone()
    return {
        "pixel_values":   pixel_values,
        "input_ids":      input_ids,
        "attention_mask": attention_mask,
        "labels":         labels,
    }

# === Step 4: Apply preprocessing ===
dataset = dataset.map(preprocess, remove_columns=["image","caption", "label"])

# === Step 5: Tell HF to return torch.Tensor for each field ===
dataset.set_format(type="torch",
                   columns=["pixel_values","input_ids","attention_mask","labels"])

# === Step 6: Training Arguments ===
training_args = TrainingArguments(
    output_dir="./blip_finetuned_output",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=5,
    save_steps=50,
    save_total_limit=1,
    remove_unused_columns=False
)

# === Step 7: Trainer ===
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=default_data_collator,
    tokenizer=processor,   # only needed for `generate()` during evaluation/logging
)

# === Step 8: Train! ===
trainer.train()

# after trainer.train()
model.save_pretrained("./blip_finetuned_output")
processor.save_pretrained("./blip_finetuned_output")

