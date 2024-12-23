import sqlite3
import random
import string
import math 
import os 
import json

DATASET_DIRECTORY = "/Users/neeraj_py/Downloads/outputacm.txt"
DATABASE_DIRECTORY = "/Users/neeraj_py/Desktop/class/Sem7/BTP/Multiplex Network Recommendation System/data/DBLP/test.db"


# NOTE: DB must be initialised using Data Preparation/DBLP/init_db.sql before running this script

'''
DATASET FORMAT
#* --- paperTitle
#@ --- Authors
#t ---- Year
#c  --- publication venue
#index 00---- index id of this paper
#% ---- the id of references of this paper (there are multiple lines, with each indicating a reference)
#! --- Abstract

eg:
#*Information geometry of U-Boost and Bregman divergence
#@Noboru Murata,Takashi Takenouchi,Takafumi Kanamori,Shinto Eguchi
#t2004
#cNeural Computation
#index436405
#%94584
#%282290
#%605546
#%620759
#%564877
#%564235
#%594837
#%479177
#%586607
#!We aim at an extension of AdaBoost to U-Boost, in the paradigm to build a stronger classification machine from a set of weak learning machines. A geometric understanding of the Bregman divergence defined by a generic convex function U leads to the U-Boost method in the framework of information geometry extended to the space of the finite measures over a label set. We propose two versions of U-Boost learning algorithms by taking account of whether the domain is restricted to the space of probability functions. In the sequential step, we observe that the two adjacent and the initial classifiers are associated with a right triangle in the scale via the Bregman divergence, called the Pythagorean relation. This leads to a mild convergence property of the U-Boost algorithm as seen in the expectation-maximization algorithm. Statistical discussions for consistency and robustness elucidate the properties of the U-Boost methods based on a stochastic assumption for training data.
'''

'''
DB SCHEMA

-- Create the main table for papers
CREATE TABLE IF NOT EXISTS Papers (
    id TEXT PRIMARY KEY,          -- Paper ID
    title TEXT,                   -- Paper title
    -- keyword TEXT,                 -- Foreign key (for relational purposes)
    year INTEGER                -- Publication year
    -- author TEXT,                  -- Foreign key (for relational purposes)
    -- doi TEXT,                     -- Digital Object Identifier
   --  n_citation INTEGER            -- Number of citations
   abstract TEXT -- Abstract of the paper
);

-- Create the table for references (citation relationships)
CREATE TABLE IF NOT EXISTS Reference ( 
    paper_id TEXT,              
    reference_id TEXT,            
    PRIMARY KEY (paper_id, reference_id),  
    FOREIGN KEY (paper_id) REFERENCES Papers(id) ON DELETE CASCADE,
    FOREIGN KEY (reference_id) REFERENCES Papers(id) ON DELETE CASCADE
);

-- Create the table for authors
CREATE TABLE IF NOT EXISTS Author (
    id INTEGER PRIMARY KEY,          -- Author ID
    name TEXT,                     -- Author name
    UNIQUE (name) ON CONFLICT IGNORE
);

-- Create the linking table for papers and authors
CREATE TABLE IF NOT EXISTS Authorship (
    paper_id TEXT,                -- Paper ID (references Papers table)
    author_id INTEGER,               -- Author ID (references Author table)
    PRIMARY KEY (paper_id, author_id),  -- Composite primary key
    FOREIGN KEY (paper_id) REFERENCES Papers(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES Author(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS VENUE (
    id INTEGER PRIMARY KEY,          -- Venue ID
    name TEXT, -- Venue name (e.g., journal or conference)
    UNIQUE (name) ON CONFLICT IGNORE 
);

CREATE TABLE IF NOT EXISTS PUBLISHED_IN (
    paper_id TEXT,                -- Paper ID (references Papers table)
    venue_id INTEGER,                -- Venue ID (references Venue table)
    PRIMARY KEY (paper_id, venue_id),  -- Composite primary key
    FOREIGN KEY (paper_id) REFERENCES Papers(id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES Venue(id) ON DELETE CASCADE
);
'''

class Paper:
    def __init__(self, id, title="", year=1000, abstract=""):
        self.id = id
        self.title = title
        self.year = year
        self.abstract = abstract


    def __str__(self):
        return f"Paper: {self.id} - {self.title} ({self.year})"

    def __repr__(self):
        return f"Paper: {self.id} - {self.title} ({self.year})"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "abstract": self.abstract,
            "authors": self.authors,
            "references": self.references,
            "venue": self.venue
        }

    def exists(self):
        cursor.execute("SELECT * FROM Papers WHERE id = ?", (self.id,))
        return cursor.fetchone()

    def insert(self):
        # Check if paper already exists
        # If it does, update the paper
        # If it doesn't, insert the paper
        try:
            if self.exists():
                if self.title!="": #  If paper overwriting its existing row in table made by a reference
                    cursor.execute("UPDATE Papers SET title = ?, year = ?, abstract = ? WHERE id = ?", (self.title, self.year, self.abstract, self.id))
            else:
                if self.title=="": # If paper is a reference
                    cursor.execute("INSERT INTO Papers (id) VALUES (?)", (self.id,))
                else:
                    cursor.execute("INSERT INTO Papers (id, title, year, abstract) VALUES (?, ?, ?, ?)", (self.id, self.title, self.year, self.abstract))
            conn.commit()
        except Exception as e:
            print(e)
            raise e
    
    def add_reference(self, reference_id):
        try:
            cursor.execute("INSERT INTO Reference (paper_id, reference_id) VALUES (?, ?)", (self.id, reference_id))
            conn.commit()
        except Exception as e:
            print(e)
    
    def add_author(self, author_id):
        try:
            cursor.execute("INSERT INTO Authorship (paper_id, author_id) VALUES (?, ?)", (self.id, author_id))
            conn.commit()
        except Exception as e:
            print(e)

    def add_venue(self, venue_id):
        try:
            cursor.execute("INSERT INTO PUBLISHED_IN (paper_id, venue_id) VALUES (?, ?)", (self.id, venue_id))
            conn.commit()
        except Exception as e:
            print(e)

    
class Author:
    def __init__(self, name):
        self.id = None  
        self.name = name

    def __str__(self):
        return f"Author: {self.id} - {self.name}"

    def __repr__(self):
        return f"Author: {self.id} - {self.name}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def exists(self):
        cursor.execute("SELECT * FROM Author WHERE name = ?", (self.name,))
        return cursor.fetchone()
    
    def insert(self):
        try:
            if not self.exists():
                cursor.execute("INSERT INTO Author (name) VALUES (?)", (self.name,))    
                conn.commit()
            
            cursor.execute("SELECT id FROM Author WHERE name = ?", (self.name,))
            self.id = cursor.fetchone()[0]

        except Exception as e:
            print(e)
            raise e
        return self.id


class Venue:
    def __init__(self, name):
        self.id = None
        self.name = name

    def __str__(self):
        return f"Venue: {self.id} - {self.name}"

    def __repr__(self):
        return f"Venue: {self.id} - {self.name}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def exists(self):
        cursor.execute("SELECT * FROM Venue WHERE name = ?", (self.name,))
        return cursor.fetchone()
        
    def insert(self):
        try:
            if not self.exists():
                cursor.execute("INSERT INTO VENUE (name) VALUES (?)", (self.name,))
                conn.commit()

            cursor.execute("SELECT id FROM Venue WHERE name = ?", (self.name,))
            self.id = cursor.fetchone()[0]
        except Exception as e:
            print(e)
            raise e
        return self.id
    
def parse_title(start,lines):
    end = start+1
    while lines[end][0] != '#' and lines[end][0] != '\n':
        end += 1
    return " ".join([line[2:].strip()  if line[0] == '#' else line.strip() for line in lines[start:end]])

def parse_authors(start, lines):
    end = start+1
    while lines[end][0] != '#'  and lines[end][0] != '\n':
        end += 1
    return [Author(name.strip()) for name in "".join([line[2:]  if line[0] == '#' else line for line in lines[start:end]]).split(",")] # Test this

def parse_year(start, lines):
    return int(lines[start][2:].strip())

def parse_venue(start, lines):
    end = start+1
    while lines[end][0] != '#' and lines[end][0] != '\n':
        end += 1
    return Venue("".join([line[2:]  if line[0] == '#' else line for line in lines[start:end]]))

def parse_abstract(start, lines):
    end = start+1
    while lines[end][0] != '#' and lines[end][0] != '\n':
        end += 1
    return " ".join([line[2:].strip()  if line[0] == '#' else line.strip() for line in lines[start:end]])

def parse_reference(start, lines):
    return Paper(lines[start][2:].strip(), None, None, None)


def parse_id(start, lines):
    return lines[start][6:].strip()


def parse_paper(start, lines):
    paperID = None
    title = None
    authors = []
    references = []
    venue = None
    year = None
    abstract = None
    end = start+1

    while lines[end][0] != '\n':
        end += 1

    for i in range(start, end):
        
        if lines[i][0:2] == "#*":
            title = parse_title(i, lines)
        elif lines[i][0:2] == "#@":
            authors = parse_authors(i, lines)
        elif lines[i][0:2] == "#t":
            year = parse_year(i, lines)
        elif lines[i][0:2] == "#c":
            venue = parse_venue(i, lines)
        elif lines[i][0:2] == "#!":
            abstract = parse_abstract(i, lines)
        elif lines[i][0:2] == "#%":
            references.append(parse_reference(i, lines))
        elif lines[i][0:6] == "#index":
            paperID = parse_id(i, lines)
    
    return {
        "id": paperID,
        "title": title,
        "authors": authors,
        "references": references,
        "venue": venue,
        "year": year,
        "abstract": abstract
    }


        
def extract_data():

    with open(DATASET_DIRECTORY, 'r') as f:
        # Skip first line
        f.readline()

        # Initialize variables
    
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i][0:2] == "#*":
                paper_dct = parse_paper(i, lines)
                paper = Paper(paper_dct["id"], paper_dct["title"], paper_dct["year"], paper_dct["abstract"])
                paper.insert()
                for author in paper_dct["authors"]:
                    author_id = author.insert()
                    paper.add_author(author_id)
                venue_id = paper_dct["venue"].insert()
                paper.add_venue(venue_id)
                for reference in paper_dct["references"]:
                    reference.insert()
                    paper.add_reference(reference.id)
                
                print("Inserted paper:", paper.id)


if __name__ == "__main__":
    conn = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = conn.cursor()

    # Check connection
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

    # Extract data
    extract_data()

    conn.close()
    print("Done")


            

                

            