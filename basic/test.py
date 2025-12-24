from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased-distilled-squad")
model = AutoModelForQuestionAnswering.from_pretrained("distilbert/distilbert-base-uncased-distilled-squad")

# Prepare inputs
context = "FastAPI is a modern web framework for building APIs with Python."
question = "What is FastAPI?"

inputs = tokenizer(question, context, return_tensors="pt")

# Model inference
with torch.no_grad():
    outputs = model(**inputs)

# Get start and end logits
start_logits = outputs.start_logits
end_logits = outputs.end_logits

# Find the tokens with the highest `start` and `end` scores
start_index = torch.argmax(start_logits)
end_index = torch.argmax(end_logits)

# Convert tokens back to string
answer_tokens = inputs.input_ids[0][start_index : end_index + 1]
answer = tokenizer.decode(answer_tokens)

print("Answer:", answer)
