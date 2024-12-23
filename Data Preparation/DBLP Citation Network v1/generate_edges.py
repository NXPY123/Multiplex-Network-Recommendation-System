import sqlite3
import os 


DATABASE_DIRECTORY = "/Users/neeraj_py/Desktop/class/Sem7/BTP/Multiplex Network Recommendation System/data/DBLP Citation Network v1/test.db"
EDGE_DIRECTORY = "/Users/neeraj_py/Desktop/class/Sem7/BTP/Multiplex Network Recommendation System/data/DBLP Citation Network v1/edges"

# For each pair of papers in the Papers table in the database, find the number of common authors divided by the total number of authors for the pair of papers and store it in a text file in the format paper1_id paper2_id similarity

def generate_edges_co_authorship():
    conn = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = conn.cursor()
    print("Connection successful")
    cursor.execute("SELECT id FROM papers")
    papers = cursor.fetchall()
    papers = [p[0] for p in papers]
    authors = []
    for i in range(len(papers)):
        cursor.execute("SELECT author_id FROM Authorship WHERE paper_id=?", (papers[i],))
        authors.append(cursor.fetchall())
    print("Fetched all papers")
    f = open(os.path.join(EDGE_DIRECTORY, "co_authorship_edges.txt"), "a")
    for i in range(len(papers)):
        for j in range(i+1, len(papers)):
            # find intersection of authors and union of authors by converting them to sets
            common_authors = len(set(authors[i]) & set(authors[j]))
            total_authors = len(set(authors[i] + authors[j]))
            similarity = common_authors / total_authors
            if(common_authors):
                print(f"{papers[i]} {papers[j]} {similarity}")
            f.write(f"{papers[i]} {papers[j]} {similarity}\n")
    print("All edges generated")
    conn.close()
    print("Connection closed")

#generate_edges_co_authorship()

def generate_edges_co_citation():
    conn = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = conn.cursor()
    print("Connection successful")
    cursor.execute("SELECT id FROM papers")
    papers = cursor.fetchall()
    papers = [p[0] for p in papers]
    references = []
    for i in range(len(papers)):
        cursor.execute("SELECT reference_id FROM Reference WHERE paper_id=?", (papers[i],))
        references.append(cursor.fetchall())
    print("Fetched all papers")
    f = open(os.path.join(EDGE_DIRECTORY, "co_citation_edges.txt"), "a")
    for i in range(len(papers)):
        for j in range(i+1, len(papers)):
            # find intersection of references and union of references by converting them to sets
            common_references = len(set(references[i]) & set(references[j]))
            total_references = len(set(references[i] + references[j]))
            similarity = common_references / total_references
            if(common_references):
                print(f"{papers[i]} {papers[j]} {similarity}")
            f.write(f"{papers[i]} {papers[j]} {similarity}\n")
    print("All edges generated")
    conn.close()
    print("Connection closed")

#generate_edges_co_citation()

def generate_edges_co_published():
    conn = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = conn.cursor()
    print("Connection successful")
    cursor.execute("SELECT id FROM papers")
    papers = cursor.fetchall()
    papers = [p[0] for p in papers]
    venues = []
    for i in range(len(papers)):
        cursor.execute("SELECT venue_id FROM Published_In WHERE paper_id=?", (papers[i],))
        venues.append(cursor.fetchall())
    print("Fetched all papers")
    f = open(os.path.join(EDGE_DIRECTORY, "co_published_edges.txt"), "a")
    for i in range(len(papers)):
        for j in range(i+1, len(papers)):
            # find intersection of venues and union of venues by converting them to sets
            common_venues = len(set(venues[i]) & set(venues[j]))
            total_venues = len(set(venues[i] + venues[j]))
            similarity = common_venues / total_venues
            if(common_venues):
                print(f"{papers[i]} {papers[j]} {similarity}")
            f.write(f"{papers[i]} {papers[j]} {similarity}\n")
    print("All edges generated")
    conn.close()
    print("Connection closed")

generate_edges_co_published()
