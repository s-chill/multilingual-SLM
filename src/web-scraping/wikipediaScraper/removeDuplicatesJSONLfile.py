import json

def remove_duplicates(input_file, output_file):
    unique_lines = set()

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            line = line.strip() #remove \n characters
            if line and line not in unique_lines:
                outfile.write(line + '\n')
                unique_lines.add(line)

input_jsonl = 'finalLinks.jsonl'
output_jsonl = 'processedFinalLinks.jsonl'

remove_duplicates(input_jsonl, output_jsonl)