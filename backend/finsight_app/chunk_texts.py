import os
import json
from backend.finsight_app.path_utils import PROCESSED_DATA_DIR

PROCESSED_DIR = PROCESSED_DATA_DIR  # Use PROCESSED_DATA_DIR for processed data
CHUNK_SIZE = 2000  # characters

metadata = {}

def chunk_text(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def main():
    for file in os.listdir(PROCESSED_DIR):
        if file.endswith('.txt') and '_chunk_' not in file:
            file_path = os.path.join(PROCESSED_DIR, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            chunks = chunk_text(text, CHUNK_SIZE)
            for idx, chunk in enumerate(chunks):
                chunk_filename = f"{file.replace('.txt', '')}_chunk_{idx}.txt"
                chunk_path = os.path.join(PROCESSED_DIR, chunk_filename)
                with open(chunk_path, 'w', encoding='utf-8') as cf:
                    cf.write(chunk)
                metadata[chunk_filename] = {
                    'source_file': file,
                    'chunk_number': idx,
                    'start_char': idx * CHUNK_SIZE,
                    'end_char': min((idx + 1) * CHUNK_SIZE, len(text))
                }
    # Save metadata
    meta_path = os.path.join(PROCESSED_DIR, 'chunk_metadata.json')
    with open(meta_path, 'w', encoding='utf-8') as mf:
        json.dump(metadata, mf, indent=2)
    print(f"Chunking complete. Metadata saved to {meta_path}")

if __name__ == '__main__':
    main()