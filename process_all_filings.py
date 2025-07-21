import os
import subprocess

# 1. Process all HTML filings in sec_filings subfolders
sec_filings_dir = "backend/data/sec_filings"
for company in os.listdir(sec_filings_dir):
    company_dir = os.path.join(sec_filings_dir, company)
    if os.path.isdir(company_dir):
        for fname in os.listdir(company_dir):
            if fname.endswith(".html"):
                fpath = os.path.join(company_dir, fname)
                print(f"Processing {fpath}")
                subprocess.run(["python", "-m", "backend.finsight_app.data_processor", "--input", fpath])

# 2. Process standalone HTML filings in backend/data/
data_dir = "backend/data"
for fname in os.listdir(data_dir):
    if fname.endswith(".html"):
        fpath = os.path.join(data_dir, fname)
        print(f"Processing {fpath}")
        subprocess.run(["python", "-m", "backend.finsight_app.data_processor", "--input", fpath])

# 3. Rebuild the vector index
print("Rebuilding FAISS index...")
subprocess.run(["python", "-m", "backend.finsight_app.build_faiss_index"]) 