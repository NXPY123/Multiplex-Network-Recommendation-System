import os

DIR = "/Users/neeraj_py/Desktop/class/Sem7/BTP/Multiplex Network Recommendation System/Multiplex Network Generation/Node Embedding Generation/Weighted Edges"

# for txt files in the directory, modify each line to subtract 1 from the first two numbers so that the node numbering starts from 0
for filename in os.listdir(DIR):
    if filename.endswith(".txt"):
        with open(os.path.join(DIR, filename), 'r') as f:
            lines = f.readlines()
        with open(os.path.join(DIR, filename), 'w') as f:
            for line in lines:
                line = line.split()
                line[0] = str(int(line[0]) - 1)
                line[1] = str(int(line[1]) - 1)
                f.write(" ".join(line) + "\n")

