# import sqlite3

# DATABASE_DIRECTORY = "/Users/neeraj_py/Desktop/class/Sem7/BTP/Multiplex Network Recommendation System/data/DBLP/test.db"

# def delete_paper(paper_id):
#     cursor.execute("DELETE FROM Authorship WHERE paper_id=?", (paper_id,))
#     cursor.execute("DELETE FROM Reference WHERE paper_id=?", (paper_id,))
#     cursor.execute("DELETE FROM PUBLISHED_IN WHERE paper_id=?", (paper_id,))
#     cursor.execute("DELETE FROM papers WHERE id=?", (paper_id,))
#     cursor.execute("DELETE FROM Reference WHERE reference_id=?", (paper_id,))

# def clean_dataset():
#     while(True):
#         cleaned = 0
#         papers = cursor.execute("SELECT id FROM papers").fetchall()
#         # Remove papers that do not share authorship with any other paper
#         for paper in papers:
#             paper = paper[0]
#             cursor.execute("SELECT * FROM Authorship WHERE paper_id=?", (paper,))
#             authors = cursor.fetchall()
#             authors = [a[1] for a in authors]
#             for author in authors:
#                 cursor.execute("SELECT * FROM Authorship WHERE author_id=? AND paper_id!=?", (author, paper))
#                 if cursor.fetchall():
#                     break
#             else:
#                 delete_paper(paper)
#                 cleaned += 1
#                 print(f"Deleted paper {paper}")
#                 continue

#              # Remove papers that do not have any references
#             cursor.execute("SELECT * FROM Reference WHERE paper_id=?", (paper,))
#             if not cursor.fetchall():
#                 delete_paper(paper)
#                 cleaned += 1
#                 print(f"Deleted paper {paper}")
#                 continue
        
#         if not cleaned:
#             break
#         conn.commit()

#     print("All papers cleaned")

# conn = sqlite3.connect(DATABASE_DIRECTORY)
# cursor = conn.cursor()
# clean_dataset()

# #629814


import sqlite3

DATABASE_DIRECTORY = "/Users/neeraj_py/Desktop/class/Sem7/BTP/Multiplex Network Recommendation System/data/DBLP/test.db"

def delete_paper(cursor, paper_id):
    """Deletes a paper and all related records from the database."""
    cursor.execute("DELETE FROM Authorship WHERE paper_id=?", (paper_id,))
    cursor.execute("DELETE FROM Reference WHERE paper_id=?", (paper_id,))
    cursor.execute("DELETE FROM PUBLISHED_IN WHERE paper_id=?", (paper_id,))
    cursor.execute("DELETE FROM papers WHERE id=?", (paper_id,))
    cursor.execute("DELETE FROM Reference WHERE reference_id=?", (paper_id,))

def clean_dataset():
    """Cleans the dataset by removing orphaned papers."""
    conn = sqlite3.connect(DATABASE_DIRECTORY)
    cursor = conn.cursor()
    print("Cleaning dataset...")
    try:
        while True:
            cleaned = 0

            # Identify papers with no shared authorship
            orphan_papers = cursor.execute("""
                SELECT p.id
                FROM papers p
                LEFT JOIN Authorship a ON p.id = a.paper_id
                LEFT JOIN Authorship a2 ON a.author_id = a2.author_id AND a2.paper_id != p.id
                WHERE a2.paper_id IS NULL
            """).fetchall()
           

            for paper_id, in orphan_papers:
                delete_paper(cursor, paper_id)
                cleaned += 1
                print(f"Deleted orphan paper {paper_id}")
            
            print("Orphan Papers Cleaned")

            # Identify papers with no references
            unreferenced_papers = cursor.execute("""
                SELECT p.id
                FROM papers p
                LEFT JOIN Reference r ON p.id = r.paper_id
                WHERE r.paper_id IS NULL
            """).fetchall()

            for paper_id, in unreferenced_papers:
                delete_paper(cursor, paper_id)
                cleaned += 1
                print(f"Deleted unreferenced paper {paper_id}")

            print("Unreferenced Papers Cleaned")
            
            if not cleaned:
                break

            conn.commit()

        print("All papers cleaned")

    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()

clean_dataset()
