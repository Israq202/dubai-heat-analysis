from transformers import pipeline

# Replace with the actual model ID on HF
model_id = "mistralai/Mistral-7B-Instruct-v0.3"

# Create a text-generation pipeline
chatbot = pipeline("text-generation", model=model_id, device=-1)  # device=-1 forces CPU / remote inference

# Example prompt
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain quantum computing in simple terms."},
]

# Generate response
response = chatbot(messages, max_new_tokens=256, do_sample=True, temperature=0.7)

print(response[0]['generated_text'])

