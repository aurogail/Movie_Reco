from sqlalchemy import create_engine, text
import pandas as pd
import os
from datetime import datetime

username = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DB')

host = '127.0.0.1'
port = '5432'  # default PostgreSQL port is 5432

# Create the database engine
try:
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
    print('Connection to database succeeded')
except Exception as e:
    print(e)
    print('Connection to database failed')

def sql(query):
    with engine.connect() as conn:
        conn.execute(text(query))

def execute_pgsql_query(filename):
    with open(filename, 'r') as file:
        query = file.read()
    sql(query)


def init_csv_to_sql(table_name, csv_path, mapping):
    df = pd.read_csv(csv_path)
    df = df.rename(columns = mapping)
    #df = df.head(100000)
    now = datetime.now()
    df['updated_at'] = now

    try:
        print(f'Injecting initial data into {table_name}')
        df.to_sql(table_name, engine, if_exists='append', index=False)
    except Exception as e:
        print(e)
        print(f'Injection of table {table_name} failed')

def create_initial_users():
    users = pd.read_csv('../raw/ratings.csv')
    users = users.drop(columns = {'movieId', 'rating', 'timestamp'})
    users = users.drop_duplicates()
    now = datetime.now()
    users['user_key'] = users['userId']        # To be encoded later ?
    users['updated_at'] = now

    try:
        print(f'Injecting initial data into users')
        users.to_sql("users", engine, if_exists='append', index=False)
    except Exception as e:
        print(e)
        print(f'Injection of table users failed')


####### 

# execute_pgsql_query("drop_database.pgsql")

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
