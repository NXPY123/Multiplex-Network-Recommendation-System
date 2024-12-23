import sqlite3
import random
import string
import math 
import os 
import json

DB_PATH = "../test.db" # Replace with the path to the database file
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check connection
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

DATASET_PATH  = "/Users/neeraj_py/Desktop/class/Sem7/BTP/Multiplex Network Recommendation System/data/split/split_0.json"

'''
DATASET FORMAT
{
  "id": "5390878320f70186a0d32f42",
  "title": "Circuit Preserving Edge Maps II",
  "abstract": "The results obtained in this paper grew from an attempt to generalize the main theorem of [1]. There it was shown that any circuit injection (a 1-1 onto edge map f such that if C is a cir
cuit then f(C) is a circuit) from a 3-connected, not necessarily finite graph G onto a graph H is induced by a vertex isomorphism, where H is assumed to not have any isolated vertices. In the present ar
ticle we examine the situation when the 1-1 condition is dropped (Chapter 1). An interesting result then is that the theorem remains true for finite (3-connected) graphs G but not for infinite G. In Cha
pter 2 we retain the 1-1 condition but allow the image of f to be first an arbitrary matroid and second a binary matroid. An interesting result then is the following. Let G be a graph of even order. The
n the statement \"no nontrivial map f:=>M exists, where M is a binary matroid\" is equivalent to \"G is Hamiltonian\". If G is a graph of odd order, then the statement \"no nontrivial map f:G=>M exists,
 where M is a binary matroid\" is equivalent to \"G is almost Hamiltonian\", where we define a graph G of order n to be almost Hamiltonian if every subset of vertices of order n-1 is contained in some c
ircuit of G. [1] J.H. Sanders and D. Sanders, Circuit preserving edge maps, J. Combin. Theory Ser. B 22 (1977),91-96.",
  "keywords": [
    "edge maps II"
  ],
  "year": 2017,
  "authors": [
    {
      "id": "",
      "name": "Jon Henry Sanders",
      "org": "",
      "org_id": ""
    }
  ],
  "references": [],
  "doi": "10.1016/0095-8956(87)90036-0",
  "venue_id": "",
  "n_citation": 0,
  "venue": "J. Comb. Theory, Ser. B"
}

'''




'''
TABLES
-- Create the main table for papers
CREATE TABLE IF NOT EXISTS Papers (
    id TEXT PRIMARY KEY,          -- Paper ID
    title TEXT,                   -- Paper title
    keyword TEXT,                 -- Foreign key (for relational purposes)
    year INTEGER,                 -- Publication year
    author TEXT,                  -- Foreign key (for relational purposes)
    doi TEXT,                     -- Digital Object Identifier
    n_citation INTEGER            -- Number of citations
);

-- Create the table for references (citation relationships)
CREATE TABLE IF NOT EXISTS Reference ( 
    paper_id TEXT,              
    reference_id TEXT,            
    PRIMARY KEY (paper_id, reference_id),  
    FOREIGN KEY (paper_id) REFERENCES Papers(id),
    FOREIGN KEY (reference_id) REFERENCES Papers(id)
);

-- Create the table for keywords
CREATE TABLE IF NOT EXISTS Keywords (
    id TEXT PRIMARY KEY,          -- Keyword ID
    keyword TEXT                  -- Keyword text
);

-- Create the linking table for papers and keywords
CREATE TABLE IF NOT EXISTS Glossary (
    paper_id TEXT,                -- Paper ID (references Papers table)
    keyword_id TEXT,              -- Keyword ID (references Keywords table)
    PRIMARY KEY (paper_id, keyword_id),  -- Composite primary key
    FOREIGN KEY (paper_id) REFERENCES Papers(id),
    FOREIGN KEY (keyword_id) REFERENCES Keywords(id)
);

-- Create the table for venues
CREATE TABLE IF NOT EXISTS Venue (
    id TEXT PRIMARY KEY,          -- Venue ID
    name TEXT                     -- Venue name (e.g., journal or conference)
);

-- Create the linking table for papers and venues
CREATE TABLE IF NOT EXISTS Presented_At (
    paper_id TEXT,                -- Paper ID (references Papers table)
    venue_id TEXT,                -- Venue ID (references Venue table)
    PRIMARY KEY (paper_id, venue_id),  -- Composite primary key
    FOREIGN KEY (paper_id) REFERENCES Papers(id),
    FOREIGN KEY (venue_id) REFERENCES Venue(id)
);

-- Create the table for authors
CREATE TABLE IF NOT EXISTS Author (
    id TEXT PRIMARY KEY,          -- Author ID
    name TEXT                     -- Author name
);

-- Create the linking table for papers and authors
CREATE TABLE IF NOT EXISTS Authorship (
    paper_id TEXT,                -- Paper ID (references Papers table)
    author_id TEXT,               -- Author ID (references Author table)
    PRIMARY KEY (paper_id, author_id),  -- Composite primary key
    FOREIGN KEY (paper_id) REFERENCES Papers(id),
    FOREIGN KEY (author_id) REFERENCES Author(id)
);

-- Create the table for organizations
CREATE TABLE IF NOT EXISTS Organisation (
    id TEXT PRIMARY KEY,          -- Organisation ID
    name TEXT                     -- Organisation name
);

-- Create the linking table for authors and organisations
CREATE TABLE IF NOT EXISTS Part_Of (
    author_id TEXT,               -- Author ID (references Author table)
    organisation_id TEXT,         -- Organisation ID (references Organisation table)
    PRIMARY KEY (author_id, organisation_id),  -- Composite primary key
    FOREIGN KEY (author_id) REFERENCES Author(id),
    FOREIGN KEY (organisation_id) REFERENCES Organisation(id)
);

-- Create the table for parent organizations associated with papers
CREATE TABLE IF NOT EXISTS Published_Under (
    paper_id TEXT,                -- Paper ID (references Papers table)
    org_id TEXT,                  -- Organisation ID (references Organisation table)
    PRIMARY KEY (paper_id, org_id),  -- Composite primary key
    FOREIGN KEY (paper_id) REFERENCES Papers(id),
    FOREIGN KEY (org_id) REFERENCES Organisation(id)
);
'''




class Paper:

    def __init__(self,paper_data):
        
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

        #print(self.id,self.title,self.abstract,self.keywords,self.year,self.authors,self.references,self.doi,self.venue_id,self.n_citation,self.venue)

    def insert_paper(self):

        # Check if paper with id exists. If yes, update the paper. Else, insert the paper
        try:
            cursor.execute("SELECT * FROM Papers WHERE id = ?",(self.id,))
            result = cursor.fetchone()
            if result:
                cursor.execute("UPDATE Papers SET title = ?, year = ?, doi = ?, n_citation = ? WHERE id = ?",(self.title,self.year,self.doi,self.n_citation,self.id))
            else:
                cursor.execute("INSERT INTO Papers (id,title,year,doi,n_citation) VALUES (?,?,?,?,?)",(self.id,self.title,self.year,self.doi,self.n_citation))

        except Exception as e:
            print(e)
    
    def insert_references(self):

        # Check if reference exists in papers table. If yes, insert the reference. Else, insert the reference id into the paper table and insert the reference into the reference table
        try:
            for reference in self.references:
                
                cursor.execute("SELECT * FROM Papers WHERE id = ?",(reference,))
                result = cursor.fetchone()
                if result:
                    cursor.execute("INSERT INTO Reference (paper_id,reference_id) VALUES (?,?)",(self.id,reference))
                else:
                    cursor.execute("INSERT INTO Papers (id) VALUES (?)",(reference,))
                    cursor.execute("INSERT INTO Reference (paper_id,reference_id) VALUES (?,?)",(self.id,reference))
        
        except Exception as e:
            print(e)
    
    def insert_keywords(self):
            
        # Check if keyword exists in keywords table. If yes, insert the keyword. Else, insert the keyword id into the paper table and insert the keyword into the keywords table

        try:
            for keyword in self.keywords:

                keyword_id = None
                cursor.execute("SELECT * FROM Keywords WHERE keyword = ?",(keyword,))
                result = cursor.fetchone()
                if result:
                    cursor.execute("INSERT INTO Glossary (paper_id,keyword_id) VALUES (?,?)",(self.id,result[0]))
                else:
                    # generate a random id for the keyword
                    keyword_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    cursor.execute("INSERT INTO Keywords (id, keyword) VALUES (?,?)",(keyword_id,keyword))
                    cursor.execute("INSERT INTO Glossary (paper_id,keyword_id) VALUES (?,?)",(self.id,keyword_id))
        
        except Exception as e:
            print(e)
    
    def insert_authors(self):
                
        # Check if author exists in authors table. If yes, insert the author. Else, insert the author id into the paper table and insert the author into the authors table

       
            for author in self.authors:
                try:
                    author_id = None
                    # Check if id exists in author table.  If yes don't insert the author. Else, insert the author id into the paper table and insert the author into the author table
                    if author["id"]:
                        cursor.execute("SELECT * FROM Author WHERE id = ?",(author["id"],))
                    else:
                        cursor.execute("SELECT * FROM Author WHERE name = ?",(author["name"],))
                    result = cursor.fetchone()

                    if result:
                        cursor.execute("INSERT INTO Authorship (paper_id,author_id) VALUES (?,?)",(self.id,result[0]))
                        author_id = result[0]
                    else:

                        # If author_id is present use it. Else, generate a random id for the author
                        if author["id"]:
                            author_id = author["id"]
                        else:
                            author_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

                        cursor.execute("INSERT INTO Author (id, name) VALUES (?,?)",(author_id,author["name"],))
                        cursor.execute("INSERT INTO Authorship (paper_id,author_id) VALUES (?,?)",(self.id,author_id))
                
                except Exception as e:
                    print(e)
                    
                author_id = author_id if author_id else result[0]
                # Check if the author is associated with an organization. If yes, insert the organization. Else, insert the organization id into the author table and insert the organization into the organization table
                try:
                    if author["org"]:
                        org_id = None

                        # Check if organization exists in organization table. If yes, insert the organization. Else, insert the organization id into the author table and insert the organization into the organization table
                        if author["org_id"]:
                            cursor.execute("SELECT * FROM Organisation WHERE id = ?",(author["org_id"],))
                        else:
                            cursor.execute("SELECT * FROM Organisation WHERE name = ?",(author["org"],))
                        result = cursor.fetchone()

                        if result:
                            cursor.execute("INSERT INTO Part_Of (author_id,organisation_id) VALUES (?,?)",(author_id,result[0]))
                            org_id = result[0]
                        else:
                            # generate a random id for the organization
                            if author["org_id"]:
                                org_id = author["org_id"]
                            else:
                                org_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                            cursor.execute("INSERT INTO Organisation (id,name) VALUES (?,?)",(org_id,author["org"],))
                            cursor.execute("INSERT INTO Part_Of (author_id,organisation_id) VALUES (?,?)",(author_id,org_id))
                        
                        # Check if the organisation is already associated with the paper. If not, insert the organization id into the paper table and insert the organization into the published_under table
                        cursor.execute("SELECT * FROM Published_Under WHERE paper_id = ? AND org_id = ?",(self.id,org_id))
                        result = cursor.fetchone()
                        if not result:
                            cursor.execute("INSERT INTO Published_Under (paper_id,org_id) VALUES (?,?)",(self.id,org_id))
                
                except Exception as e:
                    print(e)
        

    def insert_venue(self):
            
        # Check if venue id is blank. If yes, insert the venue and get the venue id. Else, insert the venue id into the paper table and insert the venue into the venue table
        
        try:

            if self.venue_id:
                cursor.execute("SELECT * FROM Venue WHERE id = ?",(self.venue_id,))
                result = cursor.fetchone()
                if result:
                    cursor.execute("INSERT INTO Presented_At (paper_id,venue_id) VALUES (?,?)",(self.id,self.venue_id))
                else:
                    cursor.execute("INSERT INTO Venue (id,name) VALUES (?,?)",(self.venue_id,self.venue))
                    cursor.execute("INSERT INTO Presented_At (paper_id,venue_id) VALUES (?,?)",(self.id,self.venue_id))
            else:
                # generate a random id for the venue
                venue_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                cursor.execute("INSERT INTO Venue (id, name) VALUES (?,?)",(venue_id,self.venue))
                cursor.execute("INSERT INTO Presented_At (paper_id,venue_id) VALUES (?,?)",(self.id,venue_id))

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

    def set_paper(self,paper_data):
        self.paper = Paper(paper_data)
    
    def insert_paper(self):
        self.paper.insert_all()




limit = math.inf # Limit the number of records to be inserted to test the code
paper_factory = PaperFactory()
# # Update the db_added.txt file with the id of the paper that has been added to the database
# with open ("db_added.txt","r") as f:
#     db_added = f.readlines()
#     # Remove the newline character
#     db_added = [x.strip() for x in db_added]

with open(DATASET_PATH) as f:
    for line in f:
        try:
            data = json.loads(line)

            paper_factory.set_paper(data)
            paper_factory.insert_paper()
            conn.commit()

        except json.JSONDecodeError:
            continue
        
        limit -= 1
        if limit == 0:
            break
with open("db_added.txt","a") as f:
    f.write(DATASET_PATH + "\n")    

#db_added.close()
