import os
import json
import matplotlib.pyplot as plt

# Directory containing JSON files
directory = '../data/split'

# Lists to store counts of authors, references, and keywords
num_authors = []
num_references = []
num_keywords = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('split_0.json'):
        filepath = os.path.join(directory, filename)
        
        # Open the file and read it incrementally with ijson
        with open(filepath, 'r') as file:
            # Initialize the JSON parser to parse the file incrementally

            for js in file:
                obj = json.loads(js)

                # Extract the necessary fields
                num_authors.append(len(obj.get('authors', [])))
                num_references.append(len(obj.get('references', [])))
                num_keywords.append(len(obj.get('keywords', [])))

# Plot the distributions
fig, axs = plt.subplots(1, 1, figsize=(18, 5))

# Plot number of authors
# axs.hist(num_authors, bins=range(0, 5), edgecolor='black', alpha=0.7)
# axs.set_title('Distribution of Papers by Number of Authors')
# axs.set_xlabel('Number of Authors')
# axs.set_ylabel('Count of Papers')

# # Plot number of references
# axs.hist(num_references, bins=range(0, 50, 5), edgecolor='black', alpha=0.7)
# axs.set_title('Distribution of Papers by Number of References')
# axs.set_xlabel('Number of References')
# axs.set_ylabel('Count of Papers')

# # Plot number of keywords
axs.hist(num_keywords, bins=range(0, 100), edgecolor='black', alpha=0.7)
axs.set_title('Distribution of Papers by Number of Keywords')
axs.set_xlabel('Number of Keywords')
axs.set_ylabel('Count of Papers')

# Show the plot
plt.tight_layout()
plt.show()