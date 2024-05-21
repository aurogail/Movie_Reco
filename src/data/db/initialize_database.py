from database_functions import execute_pgsql_query, init_csv_to_sql, create_initial_users, get_engine

# If database must be cleaned, uncomment below
# execute_pgsql_query("drop_database.pgsql")

# Use SQL Alchemy engine
engine = get_engine()

# Creates tables in the database
execute_pgsql_query("initialize_database.pgsql")

### INSERT movies.csv to recofilm_db > movies
mapping_movies = {
    'movieId': 'movie_id',
    'title': 'title',
    'genres': 'genres'    
    }

init_csv_to_sql(table_name="movies", csv_path="../raw/movies.csv", mapping=mapping_movies)

### INSERT ratings.csv to recofilm_db > ratings
mapping_ratings = {
    'userId': 'user_id',
    'movieId': 'movie_id',
    'rating': 'rating',
    'timestamp': 'created_at',    
    }

init_csv_to_sql(table_name="ratings", csv_path="../raw/ratings.csv", mapping=mapping_ratings)

### INSERT tags.csv to recofilm_db > tags
mapping_tags = {
    'userId': 'user_id',
    'movieId': 'movie_id',
    'tag': 'tag',
    'timestamp': 'created_at',    
    }

init_csv_to_sql(table_name="tags", csv_path="../raw/tags.csv", mapping=mapping_tags)

### INSERT genome-scores.csv to recofilm_db > genome_scores
mapping_gscores = {
    'movieId': 'movie_id',
    'tagId': 'gtag_id',
    'relevance': 'relevance',      
    }

init_csv_to_sql(table_name="genome_scores", csv_path="../raw/genome-scores.csv", mapping=mapping_gscores)

### INSERT genome-tags.csv to recofilm_db > genome_tags
mapping_gtags = {
    'tagId': 'gtag_id',
    'tag': 'tag',
    }

init_csv_to_sql(table_name="genome_tags", csv_path="../raw/genome-tags.csv", mapping=mapping_gtags)

### INSERT links.csv to recofilm_db > links
mapping_links = {
    'movieId': 'movie_id',
    'imdbId': 'imdb_id',
    'tmdbId': 'tmdb_id'
    }

init_csv_to_sql(table_name="links", csv_path="../raw/links.csv", mapping=mapping_links)

# INSERT DISTINCT(userId) from ratings.csv into recofilm_db > users
create_initial_users()
