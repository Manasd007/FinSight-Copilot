import os
import shutil

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SOURCE_DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
TARGET_DATA_DIR = os.path.join(PROJECT_ROOT, 'backend', 'data')

# Create target directory if it doesn't exist
os.makedirs(TARGET_DATA_DIR, exist_ok=True)

# Copy all files from source to target
def copy_data_files():
    for filename in os.listdir(SOURCE_DATA_DIR):
        source_file = os.path.join(SOURCE_DATA_DIR, filename)
        target_file = os.path.join(TARGET_DATA_DIR, filename)
        if os.path.isfile(source_file):
            shutil.copy2(source_file, target_file)
            print(f"Copied {filename} to backend/data/")
    print("✅ All data files are now in backend/data/")

if __name__ == "__main__":
    copy_data_files() 