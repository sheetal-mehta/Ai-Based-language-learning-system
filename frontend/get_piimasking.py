from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

# Load the tokenizer and model from huggingface
tokenizer_pii = AutoTokenizer.from_pretrained("Isotonic/distilbert-base-german-cased_finetuned_ai4privacy_v2")
model_pii = AutoModelForTokenClassification.from_pretrained("Isotonic/distilbert-base-german-cased_finetuned_ai4privacy_v2")

# Function to get predictions and replace tokens with labels
def replace_tokens_with_labels(text):
    # Tokenize input text
    inputs = tokenizer_pii(text, return_tensors="pt")
    
    # Performing inference here
    with torch.no_grad():
        outputs = model_pii(**inputs)
    
    # Get logits and find the predicted class
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=2)
    
    # Convert token IDs to tokens and predicted class IDs to class labels
    tokens = tokenizer_pii.convert_ids_to_tokens(inputs["input_ids"][0])
    labels = [model_pii.config.id2label[prediction.item()] for prediction in predictions[0]]
    
    # Replace tokens with labels where label is not "O", and filter out [CLS] and [SEP]
    result = []
    for token, label in zip(tokens, labels):
        if token not in ["[CLS]", "[SEP]"]:
            if label != "O":
                result.append(label)
            else:
                result.append(token)
    
    return " ".join(result)
