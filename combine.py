import os
import shutil
import torch

from torch.utils.data import Dataset, DataLoader
# from torchtune.models.llama3 import Llama3Tokenizer

from transformers import AutoTokenizer  # For tokenizing text (e.g., with HuggingFace's tokenizer)

def concat_files_single_string(input_folder="translated", output_file="concat_output.txt"):
    with open(output_file, 'wb') as output:  # Open in binary mode for direct copying
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):  # Only text files
                file_path = os.path.join(input_folder, filename)
                
                with open(file_path, 'rb') as file:  # Open each file in binary mode
                    shutil.copyfileobj(file, output)  # Copy file content to output
                
                output.write(b'\n')  # Optional: add a newline between file contents for separation

# Usage to concatenate tamil files:
# concat_files_single_string(input_folder="translated", output_file="concat_output.txt")

class TextDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=128):
        # Read and preprocess the concatenated file
        with open(file_path, 'r', encoding='utf-8') as f:
            self.text = f.read()
        
        # Split text into sentences or sequences of desired length
        self.sequences = [self.text[i:i+max_length] for i in range(0, len(self.text), max_length)]
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        # Tokenize each sequence
        
        encoded = self.tokenizer(self.sequences[idx], truncation=True, padding="max_length", max_length=self.max_length, return_tensors="pt")
        return encoded.input_ids.squeeze(), encoded.attention_mask.squeeze()

# Initialize the tokenizer (use any pre-trained model you like)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8b")  # Replace with your preferred tokenizer
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
# tokenizer = Llama3Tokenizer("/path/to/spm_model")

# Create the dataset and dataloader
file_path = "concat_output.txt"
dataset = TextDataset(file_path, tokenizer)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)  # Adjust batch size as needed

# Check a batch to confirm it works
for batch in dataloader:
    input_ids, attention_mask = batch
    print("Batch input_ids shape:", input_ids.shape)
    print("Batch attenition_mask shape:", attention_mask.shape)