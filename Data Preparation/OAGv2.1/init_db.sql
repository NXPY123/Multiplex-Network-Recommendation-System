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
    FOREIGN KEY (paper_id) REFERENCES Papers(id) ON DELETE CASCADE,
    FOREIGN KEY (reference_id) REFERENCES Papers(id) ON DELETE CASCADE
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
    FOREIGN KEY (paper_id) REFERENCES Papers(id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES Keywords(id) ON DELETE CASCADE
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
    FOREIGN KEY (paper_id) REFERENCES Papers(id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES Venue(id) ON DELETE CASCADE
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
    FOREIGN KEY (paper_id) REFERENCES Papers(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES Author(id) ON DELETE CASCADE
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
    FOREIGN KEY (author_id) REFERENCES Author(id) ON DELETE CASCADE,
    FOREIGN KEY (organisation_id) REFERENCES Organisation(id) ON DELETE CASCADE
);

-- Create the table for parent organizations associated with papers
CREATE TABLE IF NOT EXISTS Published_Under (
    paper_id TEXT,                -- Paper ID (references Papers table)
    org_id TEXT,                  -- Organisation ID (references Organisation table)
    PRIMARY KEY (paper_id, org_id),  -- Composite primary key
    FOREIGN KEY (paper_id) REFERENCES Papers(id) ON DELETE CASCADE,
    FOREIGN KEY (org_id) REFERENCES Organisation(id) ON DELETE CASCADE
);