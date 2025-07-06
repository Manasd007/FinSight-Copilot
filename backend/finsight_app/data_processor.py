import os
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.finsight_app.path_utils import DATA_DIR, PROCESSED_DATA_DIR

class DataProcessor:
    def __init__(self, input_dir=None, output_dir=None):
        self.input_dir = input_dir or DATA_DIR
        self.output_dir = output_dir or PROCESSED_DATA_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def clean_html(self, html_file):
        input_path = os.path.join(self.input_dir, html_file)
        output_path = os.path.join(self.output_dir, html_file.replace(".html", ".txt"))

        with open(input_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        text = soup.get_text(separator="\n", strip=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✅ Cleaned text saved to: {output_path}")
        return output_path

    def chunk_text(self, txt_file, chunk_size=1000, overlap=200):
        file_path = os.path.join(self.output_dir, txt_file)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        chunks = splitter.split_text(text)

        chunk_paths = []
        for i, chunk in enumerate(chunks):
            chunk_file = txt_file.replace(".txt", f"_chunk_{i}.txt")
            full_chunk_path = os.path.join(self.output_dir, chunk_file)
            with open(full_chunk_path, "w", encoding="utf-8") as f:
                f.write(chunk)
            chunk_paths.append(full_chunk_path)

        print(f"✅ {len(chunk_paths)} chunks saved to: {self.output_dir}")
        return chunk_paths 