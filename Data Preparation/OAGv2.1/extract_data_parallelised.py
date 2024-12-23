import multiprocessing
import os
import sqlite3
import random
import string
import json

LIMIT = 50000
NO_OF_PROCESSES = 10
BATCH_SIZE = LIMIT*NO_OF_PROCESSES
DATATSET_PATH = "/Users/neeraj_py/Downloads/v3.1_oag_publication_1.json"
DB_PATH = None



class Paper:

    def __init__(self,paper_data,cursor):
        
        self.id = paper_data["id"]
        self.title = paper_data["title"]
        self.abstract = paper_data["abstract"]
        self.keywords = paper_data["keywords"]
        self.year = paper_data["year"]
        self.authors = paper_data["authors"]
        self.references = paper_data["references"]
        self.doi = paper_data["doi"]
        self.venue_id = paper_data["venue_id"]
        self.n_citation = paper_data["n_citation"]
        self.venue = paper_data["venue"]
        self.cursor = cursor

        #print(self.id,self.title,self.abstract,self.keywords,self.year,self.authors,self.references,self.doi,self.venue_id,self.n_citation,self.venue)

    def insert_paper(self):

        # Check if paper with id exists. If yes, update the paper. Else, insert the paper
        try:
            self.cursor.execute("SELECT * FROM Papers WHERE id = ?",(self.id,))
            result = self.cursor.fetchone()
            if result:
                self.cursor.execute("UPDATE Papers SET title = ?, year = ?, doi = ?, n_citation = ? WHERE id = ?",(self.title,self.year,self.doi,self.n_citation,self.id))
            else:
                self.cursor.execute("INSERT INTO Papers (id,title,year,doi,n_citation) VALUES (?,?,?,?,?)",(self.id,self.title,self.year,self.doi,self.n_citation))

        except Exception as e:
            print(e)
    
    def insert_references(self):

        # Check if reference exists in papers table. If yes, insert the reference. Else, insert the reference id into the paper table and insert the reference into the reference table
        try:
            for reference in self.references:
                
                self.cursor.execute("SELECT * FROM Papers WHERE id = ?",(reference,))
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute("INSERT INTO Reference (paper_id,reference_id) VALUES (?,?)",(self.id,reference))
                else:
                    self.cursor.execute("INSERT INTO Papers (id) VALUES (?)",(reference,))
                    self.cursor.execute("INSERT INTO Reference (paper_id,reference_id) VALUES (?,?)",(self.id,reference))
        
        except Exception as e:
            print(e)
    
    def insert_keywords(self):
            
        # Check if keyword exists in keywords table. If yes, insert the keyword. Else, insert the keyword id into the paper table and insert the keyword into the keywords table

        try:
            for keyword in self.keywords:

                keyword_id = None
                self.cursor.execute("SELECT * FROM Keywords WHERE keyword = ?",(keyword,))
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute("INSERT INTO Glossary (paper_id,keyword_id) VALUES (?,?)",(self.id,result[0]))
                else:
                    # generate a random id for the keyword
                    keyword_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    self.cursor.execute("INSERT INTO Keywords (id, keyword) VALUES (?,?)",(keyword_id,keyword))
                    self.cursor.execute("INSERT INTO Glossary (paper_id,keyword_id) VALUES (?,?)",(self.id,keyword_id))
        
        except Exception as e:
            print(e)
    
    def insert_authors(self):
                
        # Check if author exists in authors table. If yes, insert the author. Else, insert the author id into the paper table and insert the author into the authors table

       
            for author in self.authors:
                try:
                    author_id = None
                    # Check if id exists in author table.  If yes don't insert the author. Else, insert the author id into the paper table and insert the author into the author table
                    if author["id"]:
                        self.cursor.execute("SELECT * FROM Author WHERE id = ?",(author["id"],))
                    else:
                        self.cursor.execute("SELECT * FROM Author WHERE name = ?",(author["name"],))
                    result = self.cursor.fetchone()

                    if result:
                        self.cursor.execute("INSERT INTO Authorship (paper_id,author_id) VALUES (?,?)",(self.id,result[0]))
                        author_id = result[0]
                    else:

                        # If author_id is present use it. Else, generate a random id for the author
                        if author["id"]:
                            author_id = author["id"]
                        else:
                            author_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

                        self.cursor.execute("INSERT INTO Author (id, name) VALUES (?,?)",(author_id,author["name"],))
                        self.cursor.execute("INSERT INTO Authorship (paper_id,author_id) VALUES (?,?)",(self.id,author_id))
                
                except Exception as e:
                    print(e)
                    
                author_id = author_id if author_id else result[0]
                # Check if the author is associated with an organization. If yes, insert the organization. Else, insert the organization id into the author table and insert the organization into the organization table
                try:
                    if author["org"]:
                        org_id = None

                        # Check if organization exists in organization table. If yes, insert the organization. Else, insert the organization id into the author table and insert the organization into the organization table
                        if author["org_id"]:
                            self.cursor.execute("SELECT * FROM Organisation WHERE id = ?",(author["org_id"],))
                        else:
                            self.cursor.execute("SELECT * FROM Organisation WHERE name = ?",(author["org"],))
                        result = self.cursor.fetchone()

                        if result:
                            self.cursor.execute("INSERT INTO Part_Of (author_id,organisation_id) VALUES (?,?)",(author_id,result[0]))
                            org_id = result[0]
                        else:
                            # generate a random id for the organization
                            if author["org_id"]:
                                org_id = author["org_id"]
                            else:
                                org_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                            self.cursor.execute("INSERT INTO Organisation (id,name) VALUES (?,?)",(org_id,author["org"],))
                            self.cursor.execute("INSERT INTO Part_Of (author_id,organisation_id) VALUES (?,?)",(author_id,org_id))
                        
                        # Check if the organisation is already associated with the paper. If not, insert the organization id into the paper table and insert the organization into the published_under table
                        self.cursor.execute("SELECT * FROM Published_Under WHERE paper_id = ? AND org_id = ?",(self.id,org_id))
                        result = self.cursor.fetchone()
                        if not result:
                            self.cursor.execute("INSERT INTO Published_Under (paper_id,org_id) VALUES (?,?)",(self.id,org_id))
                
                except Exception as e:
                    print(e)
        

    def insert_venue(self):
            
        # Check if venue id is blank. If yes, insert the venue and get the venue id. Else, insert the venue id into the paper table and insert the venue into the venue table
        
        try:

            if self.venue_id:
                self.cursor.execute("SELECT * FROM Venue WHERE id = ?",(self.venue_id,))
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute("INSERT INTO Presented_At (paper_id,venue_id) VALUES (?,?)",(self.id,self.venue_id))
                else:
                    self.cursor.execute("INSERT INTO Venue (id,name) VALUES (?,?)",(self.venue_id,self.venue))
                    self.cursor.execute("INSERT INTO Presented_At (paper_id,venue_id) VALUES (?,?)",(self.id,self.venue_id))
            else:
                # generate a random id for the venue
                venue_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                self.cursor.execute("INSERT INTO Venue (id, name) VALUES (?,?)",(venue_id,self.venue))
                self.cursor.execute("INSERT INTO Presented_At (paper_id,venue_id) VALUES (?,?)",(self.id,venue_id))

        except Exception as e:
            print(e)

    def insert_all(self):
        self.insert_paper()
        self.insert_references()
        self.insert_keywords()
        self.insert_authors()
        self.insert_venue()

class PaperFactory:

    def __init__(self):
        self.paper = None

    def set_paper(self,paper_data,cursor):
        self.paper = Paper(paper_data,cursor)
    
    def insert_paper(self):
        self.paper.insert_all()




def clean_dataset(i):
    print("Process", i, "started")

    DB_PATH = f"../data/test{i}.db"

   

    # Create a test{i}.db file if it does not exist
    if not os.path.exists(DB_PATH):
        open(DB_PATH, 'w').close()
        print(f"Created test{i}.db")
    
    # Run init_db.sql to create the schema
    with open("init_db.sql", "r") as f:
        schema = f.read()

    with sqlite3.connect(DB_PATH, timeout=10) as conn:

        cursor = conn.cursor()

        # Check if schema exists. If not, create the schema
        schema_exists = False
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            if table[0] == "Papers":
                schema_exists = True
                break
        if not schema_exists:
            cursor.executescript(schema)
            conn.commit()
            print("Schema created")
    


    
    



    conn = sqlite3.connect(DB_PATH, timeout=10)
    cursor = conn.cursor()

    # Check connection
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    try:
        cursor.fetchall()
        print("Connection successful")

    except Exception as e:
        print("Connection failed")
        raise e


    


    l = i*LIMIT
    r = l + (LIMIT-1)

    print(f"l_{i}: {l}, r_{i}: {r}")

    

    paperFactory = PaperFactory()
    
    # open dataset in read mode
    with open(DATATSET_PATH, "r") as f1:
        for line_number, line in enumerate(f1):
            if line_number < l:
                continue
                
            elif line_number >= l and line_number <= r:
                # if line_number > last_line_number:
                try:
                    paperFactory.set_paper(json.loads(line),cursor)
                    paperFactory.insert_paper()
                    conn.commit()
                    # Write the id of the paper to the dbAdded{i}.txt file
                    f.write(f"{json.loads(line)['id']}\n")    
                    print(f"Inserted paper {json.loads(line)['id']}")

                except Exception as e:
                    print(e)
                    pass
        
            else:
                l = LIMIT*NO_OF_PROCESSES  + l
                r = l + (LIMIT-1)




if __name__ == '__main__':

    manager = multiprocessing.Manager()
    processes = []

    # Create a ../data directory if it does not exist
    if not os.path.exists("../data"):
        os.makedirs("../data")

    for i in range(NO_OF_PROCESSES):
        p = multiprocessing.Process(target=clean_dataset, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
        print("Process", p, "joined")

    

    
