CREATE TABLE wiki_summaries (
    uuid VARCHAR(255) PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);