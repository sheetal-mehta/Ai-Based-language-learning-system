"""
Script to download and store the falko merlin dataset from huggingface.
"""
from datasets import load_dataset

def save_splits(dataset_name, save_path):
    # Load the dataset
    dataset = load_dataset(dataset_name)

    # Convert and save train, test, and validation splits to JSON
    dataset["train"].to_json(f"{save_path}/train.json")
    dataset["test"].to_json(f"{save_path}/test.json")
    dataset["validation"].to_json(f"{save_path}/validation.json")

if __name__ == "__main__":
    dataset_name = "matejklemen/falko_merlin"  # Specify the name of the dataset you want to download
    save_path = "D:/SRH Study Data/SEM 04/Master's Thesis/Datat1/falko-merlin"  # Specify the directory where you want to save the dataset
    save_splits(dataset_name, save_path)
