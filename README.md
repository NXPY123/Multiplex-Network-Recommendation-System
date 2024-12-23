
## Data Preparation

### Extract Data 

The data is extracted from the following sources:
[DBLP Citation Network V10](https://www.aminer.cn/citation)

To extract the data from the source, we use the following steps:

1. Download the data from the source
The Dataset should be a JSON file with the following format:

```json
DATASET FORMAT
{
  "id": string,
  "title": string,
  "abstract": string,
  "keywords": List[string],
  "year": int,
  "authors": List[dict({"id": string, "name": string, "org": string, "org_id": string})],
  "references": List[string],
  "doi": string,
  "venue_id": string,
  "n_citation": int,
  "venue": string,
}
`
``

2. Replace the `dataset_path` variable in the `extract_data.py` file with the path to the downloaded dataset.


3. Initialise tables in the database using the sql script `init_db.sql`

4. Set the `DB_PATH` variable in the `extract_data.py` file to the path of the database.

5. Run the `extract_data.py` file to extract the data from the dataset and store it in the database.



