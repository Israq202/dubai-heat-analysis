from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
import torch
import os

# Path to your downloaded Llama 2 model
model_path = "/Users/Qasem/mistral_models/Llama-2-7b-hf"

# Verify required files exist
required_files = ["config.json", "pytorch_model.bin", "tokenizer.model"]
missing_files = [f for f in required_files if not os.path.exists(os.path.join(model_path, f))]
if missing_files:
    raise FileNotFoundError(f"Missing files in model folder: {missing_files}")

# Load tokenizer and model offline
tokenizer = LlamaTokenizer.from_pretrained(model_path, local_files_only=True)
model = LlamaForCausalLM.from_pretrained(
    model_path,
    local_files_only=True,
    device_map="auto"  # Automatically uses GPU if available
)

# Create a text-generation pipeline
chat = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Simple chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    output = chat(
        user_input,
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7
    )
    print("Llama2:", output[0]["generated_text"])




