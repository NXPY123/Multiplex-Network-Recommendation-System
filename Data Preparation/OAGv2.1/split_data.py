import json
import os

DATASET_PATH  = "/Users/neeraj_py/Downloads/v3.1_oag_publication_1.json"
DATA_DIR = "../data"
SPLIT_NO = 10
SPLIT_DIR = os.path.join(DATA_DIR, "split")
FILE_NAMES = [f"split_{i}.json" for i in range(SPLIT_NO)]

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SPLIT_DIR, exist_ok=True)
# Create files in split directory if they don't exist
for file_name in FILE_NAMES:
    open(os.path.join(SPLIT_DIR, file_name), 'w').close()

l = 0
with open(DATASET_PATH, 'r') as f:
    for json_obj in f:
        with open(os.path.join(SPLIT_DIR, FILE_NAMES[l % SPLIT_NO]), 'a') as split_file:
            split_file.write(json_obj)
        l += 1
print("Split the dataset successfully!")

