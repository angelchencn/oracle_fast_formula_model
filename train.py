import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

# Configuration
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"
DATA_PATH = [
    "data/processed/bonus_data.jsonl",
    "data/processed/absence_data.jsonl",
    "data/processed/overtime_data.jsonl"
]
OUTPUT_DIR = "output"

def train():
    print(f"Loading model: {MODEL_NAME}")
    
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        trust_remote_code=True
    )
    model.config.use_cache = False

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    # LoRA config
    peft_config = LoraConfig(
        lora_alpha=16,
        lora_dropout=0.1,
        r=64,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    )

    # Load dataset
    dataset = load_dataset("json", data_files=DATA_PATH, split="train")

    # Training arguments
    training_args = SFTConfig(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=10,
        max_steps=50, # Short run for demo/testing
        save_steps=25,
        fp16=True,
        optim="paged_adamw_32bit",
        dataset_text_field="output", # Using output as the text field for now
        max_length=512,
        packing=False,
    )

    # Trainer
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        processing_class=tokenizer,
        args=training_args,
    )

    print("Starting training...")
    trainer.train()
    
    print(f"Saving model to {OUTPUT_DIR}")
    trainer.save_model(OUTPUT_DIR)

if __name__ == "__main__":
    train()
