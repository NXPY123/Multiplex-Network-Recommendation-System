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

# Fetch all papers
cursor.execute("SELECT id FROM papers")
papers = cursor.fetchall()
papers = set(p[0] for p in papers)


def delete_paper(paper_id):
    cursor.execute("DELETE FROM Authorship WHERE paper_id=?", (paper_id,))
    cursor.execute("DELETE FROM Reference WHERE paper_id=?", (paper_id,))
    cursor.execute("DELETE FROM Glossary WHERE paper_id=?", (paper_id,))
    cursor.execute("DELETE FROM papers WHERE id=?", (paper_id,))
    conn.commit()

for paper in papers:

    # Remove all papers that have no authorship
    cursor.execute("SELECT * FROM Authorship WHERE paper_id=?", (paper,))
    if not cursor.fetchall():
        delete_paper(paper)
        #cleaned.append(paper)
        print(f"Deleted paper {paper}")
    
    # Remove all papers that have no citation
    cursor.execute("SELECT * FROM Reference WHERE paper_id=?", (paper,))
    if not cursor.fetchall():
        delete_paper(paper)
        #cleaned.append(paper)
        print(f"Deleted paper {paper}")
    else:
        # Check if the citations are valid
        cursor.execute("SELECT * FROM Reference WHERE paper_id=?", (paper,))
        references = cursor.fetchall()
        references = [r[1] for r in references]
        for reference in references:
            cursor.execute("SELECT * FROM papers WHERE id=?", (reference,))
            if not cursor.fetchall():
                # Delete the reference
                cursor.execute("DELETE FROM Reference WHERE paper_id=? AND reference_id=?", (paper, reference))
                conn.commit()
        # Check if the paper has any references left
        cursor.execute("SELECT * FROM Reference WHERE paper_id=?", (paper,))
        if not cursor.fetchall():
            delete_paper(paper)
            #cleaned.append(paper)
            print(f"Deleted paper {paper}")

        
        # Remove all papers that have no keyword
        cursor.execute("SELECT * FROM Glossary WHERE paper_id=?", (paper,))
        if not cursor.fetchall():
            delete_paper(paper)
            #cleaned.append(paper)
            print(f"Deleted paper {paper}")



while(True):
    cleaned = []
    # Remove papers that do not share authorship with any other paper
    for paper in papers:
        cursor.execute("SELECT * FROM Authorship WHERE paper_id=?", (paper,))
        authors = cursor.fetchall()
        authors = [a[1] for a in authors]
        for author in authors:
            cursor.execute("SELECT * FROM Authorship WHERE author_id=? AND paper_id!=?", (author, paper))
            if cursor.fetchall():
                break
        else:
            delete_paper(paper)
            cleaned.append(paper)
            print(f"Deleted paper {paper}")

    print("All papers cleaned")

    # Remove papers that do not share any keyword with any other paper
    for paper in papers:
        cursor.execute("SELECT * FROM Glossary WHERE paper_id=?", (paper,))
        keywords = cursor.fetchall()
        keywords = [k[1] for k in keywords]
        for keyword in keywords:
            cursor.execute("SELECT * FROM Glossary WHERE keyword_id=? AND paper_id!=?", (keyword, paper))
            if cursor.fetchall():
                break
        else:
            delete_paper(paper)
            cleaned.append(paper)
            print(f"Deleted paper {paper}")

    if not cleaned:
        break

    for paper in cleaned:
        papers.remove(paper)
        
print("All papers cleaned")


    






    