import os
import json
import csv
from bs4 import BeautifulSoup

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'processed_data')

os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_text_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Flatten and join all string fields
    def flatten(d):
        if isinstance(d, dict):
            return '\n'.join([flatten(v) for v in d.values()])
        elif isinstance(d, list):
            return '\n'.join([flatten(i) for i in d])
        elif isinstance(d, str):
            return d
        else:
            return ''
    return flatten(data)


def extract_text_from_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = ['\t'.join(row) for row in reader]
    return '\n'.join(lines)


def extract_text_from_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # Get visible text
    return soup.get_text(separator='\n', strip=True)


def process_file(filepath, rel_path):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.json':
        text = extract_text_from_json(filepath)
    elif ext == '.csv':
        text = extract_text_from_csv(filepath)
    elif ext == '.html':
        text = extract_text_from_html(filepath)
    else:
        return None, None
    # Output file name: replace / and . with _
    out_name = rel_path.replace(os.sep, '_').replace('.', '_') + '.txt'
    out_path = os.path.join(OUTPUT_DIR, out_name)
    return text, out_path


def main():
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, DATA_DIR)
            text, out_path = process_file(filepath, rel_path)
            if text and out_path:
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Extracted: {rel_path} -> {out_path}")

if __name__ == '__main__':
    main() 