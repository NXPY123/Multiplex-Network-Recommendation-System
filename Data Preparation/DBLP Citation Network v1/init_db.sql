-- Create the main table for papers
CREATE TABLE IF NOT EXISTS Papers (
    id TEXT PRIMARY KEY,          -- Paper ID
    title TEXT,                   -- Paper title
    -- keyword TEXT,                 -- Foreign key (for relational purposes)
    year INTEGER,                -- Publication year
    -- author TEXT,                  -- Foreign key (for relational purposes)
    -- doi TEXT,                     -- Digital Object Identifier
   --  n_citation INTEGER            -- Number of citations
   abstract TEXT --  Abstract of the paper
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