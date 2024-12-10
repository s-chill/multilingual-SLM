import os
import shutil

source_dir = '.'
target_dir = os.path.join(source_dir, 'data', 'htmlFiles')
os.makedirs(target_dir, exist_ok=True)

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            
            shutil.move(file_path, target_dir)

print(f"All HTML files have been moved to {target_dir}")
