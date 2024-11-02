import os
import shutil

def concat_files_single_string(input_folder="translated", output_file="output.txt"):
    with open(output_file, 'wb') as output:  # Open in binary mode for direct copying
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):  # Only text files
                file_path = os.path.join(input_folder, filename)
                
                with open(file_path, 'rb') as file:  # Open each file in binary mode
                    shutil.copyfileobj(file, output)  # Copy file content to output
                
                output.write(b'\n')  # Optional: add a newline between file contents for separation

# Usage
# concat_files_single_string(input_folder="translated", output_file="output.txt")

