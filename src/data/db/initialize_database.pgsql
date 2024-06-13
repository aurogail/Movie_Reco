CREATE TABLE movies (
    movie_id    INTEGER PRIMARY KEY,
    title       VARCHAR(255),
    genres      TEXT
);

CREATE TABLE users (
    user_id     INTEGER PRIMARY KEY,
    user_key    TEXT
);

CREATE TABLE ratings (
    /* rating_id   SERIAL PRIMARY KEY, */
    user_id     INTEGER,    
    movie_id    INTEGER,
    rating      DECIMAL(2, 1) CHECK (rating >= 0.0 AND rating <= 5.0),
    created_at  TIMESTAMP,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE links (
    /* link_id     SERIAL PRIMARY KEY, */
    movie_id    INTEGER,
    imdb_id     INTEGER,
    tmdb_id     INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

CREATE TABLE tags (
    /* tag_id      INTEGER PRIMARY KEY, */
    user_id     INTEGER,
    movie_id    INTEGER,
    tag         TEXT,
    created_at  TIMESTAMP,    
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE genome_tags (
    gtag_id     INTEGER PRIMARY KEY,
    tag         TEXT
);

CREATE TABLE genome_scores (
    movie_id    INTEGER,
    gtag_id     INTEGER,
    relevance   NUMERIC,
    FOREIGN KEY (gtag_id) REFERENCES genome_tags(gtag_id)
);

CREATE TABLE predicted_ratings (
    pred_id             SERIAL PRIMARY KEY,
    predicted_rating    NUMERIC,
    model               TEXT,
    feedback            TEXT
);

CREATE TABLE recommendations (
    reco_id         SERIAL PRIMARY KEY,
    movie_id        INTEGER,
    user_id         INTEGER,  
    reco_type       TEXT,
    reco_datetime   TIMESTAMP,
    user_feedback   INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_ratings_movieId ON ratings(movie_id);
CREATE INDEX idx_ratings_userId ON ratings(user_id);