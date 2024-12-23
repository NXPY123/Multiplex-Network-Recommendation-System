import sqlite3
from collections import defaultdict

DB_PATH = "../test.db" # Replace with the path to the database file
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check connection
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
try:
    cursor.fetchall()
    print("Connection successful")
except Exception as e:
    print("Connection failed")
    raise e

# Get all citations
cursor.execute("SELECT paper_id, reference_id FROM Reference")
citations = cursor.fetchall()
print("Citations fetched")

# if authorships.txt does not exist, create it
try:
    open("citations.txt", "x")
except:
    print("File already exists")

# Get the last line of the file
with open("citations.txt", "r") as f:
    try:
        last_line = f.readlines()[-1]
        last_line = last_line.strip()
        last_line = last_line.split(" ")
        last_line = (last_line[0], last_line[1]) 
    except:
        last_line = (None, None)   

# Find the index of the last line in the list of citations
if last_line[0] is not None:
    index = citations.index(last_line)
else:
    index = -1
print("Index found")

# Add citations to the file
citations_file = open("citations.txt", "a")
for index in range(index+1, len(citations)): # This may lead to duplicates as we're iterating from the last line
    citation = citations[index]
    citations_file.write(f"{citation[0]} {citation[1]} 1\n")
citations_file.close()
print("Citations added to file")


# if citations_index_based.txt does not exist, create it
try:
    open("citations_index_based.txt", "x")
except:
    print("File already exists")

# Get papers
cursor.execute("SELECT id FROM papers")
papers = cursor.fetchall()
papers = [p[0] for p in papers]
print("Papers fetched")

# Make index mapping to paper id
paper_index = {}
for i in range(len(papers)):
    paper_index[papers[i]] = i  

# Get the last line of the file
with open("citations_index_based.txt", "r") as f:
    try:
        last_line = f.readlines()[-1]
        last_line = last_line.strip()
        last_line = last_line.split(" ")
        last_line = (last_line[0], last_line[1])
    except:
        last_line = (-1,-1)

# Find the index of the last line in the list of papers
if last_line[1] != -1:
    paper1 = papers[last_line[0]]
    paper2 = papers[last_line[1]]
    idx = citations.index((paper1, paper2))
else:
    idx = -1

print("Index found")

# Add citations to the file
citations_file = open("citations_index_based.txt", "a")
for i in range(idx+1, len(citations)):
    citation = citations[i]
    citations_file.write(f"{paper_index[citation[0]]} {paper_index[citation[1]]}\n") # No edge weights for now
citations_file.close()

print("Citations added to file")




