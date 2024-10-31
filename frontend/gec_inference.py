import torch
from transformers import MT5ForConditionalGeneration, MT5Tokenizer
from difflib import ndiff

# Path to the directory where the finetuned gec model and tokenizer are saved
model_dir = './mt5-base-2'

# Load the tokenizer and model
tokenizer = MT5Tokenizer.from_pretrained(model_dir)
model = MT5ForConditionalGeneration.from_pretrained(model_dir)

# Define the function to generate corrected sentences
def correct_sentences(input_sentences, tokenizer, model):
    # Tokenize the input sentences
    inputs = tokenizer(input_sentences, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Generate predictions
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512, num_beams=5, early_stopping=True)

    # Decode the predictions
    corrected_sentences = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    
    return corrected_sentences

# Function to highlight differences
def highlight_differences(sent1, sent2):
    diff = list(ndiff(sent1.split(), sent2.split()))
    highlighted_text = ""

    for word in diff:
        # Filter for additions in the second sentence and ignore deletions
        if word.startswith("+ "):
            highlighted_text += f'<span style="color: green;">{word[2:]}</span> '
        elif word.startswith("  "):  # unchanged words
            highlighted_text += word[2:] + " "

    # Remove any trailing spaces or extra characters
    highlighted_text = highlighted_text.rstrip()

    return highlighted_text
