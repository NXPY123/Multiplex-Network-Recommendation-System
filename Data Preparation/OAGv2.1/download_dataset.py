# import json
import os
import requests
import zipfile

URL = "https://opendata.aminer.cn/dataset/v3.1_oag_publication_1.zip"
FILE_NAME = "v3.1_oag_publication_1.zip"
DATA_DIR = "../data"

# Create data directory
os.makedirs(DATA_DIR, exist_ok=True)

# Download the dataset
def download_file(url, local_filename):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
                # Print download progress
                print(f"Downloading {local_filename} {os.path.getsize(local_filename)} bytes", end='\r')
    print(end='\n')
    return local_filename

# Extract the dataset
def extract_dataset(file_path):
 
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
    print("Extracted the dataset successfully!")


download_file(URL, os.path.join(DATA_DIR, FILE_NAME))
print("Downloaded the dataset successfully!")

extract_dataset(os.path.join(DATA_DIR, FILE_NAME))
print("Extracted the dataset successfully!")

os.remove(os.path.join(DATA_DIR, FILE_NAME))
print("Deleted the zip file successfully!")

