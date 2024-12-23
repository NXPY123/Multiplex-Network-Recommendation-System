
## Data Preparation

### Extract Data 

The data is extracted from the following sources:
[DBLP Citation-network v1](https://www.aminer.cn/citation)

To extract the data from the source, we use the following steps:

1. Download the data from the source
The Dataset should be a txt file with the following format:

```
DATASET FORMAT
#* --- paperTitle
#@ --- Authors
#t ---- Year
#c  --- publication venue
#index 00---- index id of this paper
#% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
#! --- Abstract
```

2. Place the dataset in the `data/DBLP Citation Network v1/` folder

3. Create a `test.db` file in the `data/DBLP Citation Network v1/` folder using the following command:

```bash
cd "./Multiplex Network Recommendation System"
sqlite3 "./data/DBLP Citation Network v1/test.db" < "./Data Preparation/DBLP Citation Network v1/init_db.sql"
```

4. Create a virtual environment and install the required packages using the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Run the following command to extract the data from the dataset:

```bash
python "./Data Preparation/DBLP Citation Network v1/extract_data.py"
```

6. The data will be extracted and stored in the `test.db` file in the `data/` folder.

7. Clean the data using the following command:

```bash
python "./Data Preparation/DBLP Citation Network v1/clean_data.py"
```

8. The data will be cleaned and stored in the `test.db` file in the `data/` folder.

9. Generate edges for the data using the following command:

```bash
python "./Data Preparation/DBLP Citation Network v1/generate_edges.py"
```

10. The edges will be generated and stored in the `data/DBLP Citation Network v1/edges/` directory.

11. Generate node embeddings for the data by placing the .txt edge files in the `Multiplex Network Generation/Node Embedding Generation/volume/Weighted Edges` folder and running the following command:

```bash
cd "./Multiplex Network Generation/Node Embedding Generation"
docker-compose up
```

12. The node embeddings will be generated and stored in the `Multiplex Network Generation/Node Embedding Generation/volume/Node Embeddings` directory.



