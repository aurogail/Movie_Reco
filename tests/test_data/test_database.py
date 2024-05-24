import logging
import pandas as pd
from datetime import datetime
from sqlalchemy import inspect
from src.data.db.database_functions import get_engine

path = "src/data/raw"
current_time = datetime.now()
current_ts = current_time.timestamp()
min_expected_ts = datetime(1995, 1, 1, 0, 0, 0).timestamp()           # we don't expect data prior to 1995

logger = logging.getLogger("airflow.task")

# Use SQL Alchemy engine
engine, inspector = get_engine()

def check_table_details(table_name, expected_schema):

    engine, inspector = get_engine()
    columns = inspector.get_columns(table_name)

    for column in columns:
            column_name = column['name']
            assert column_name in expected_schema, f"Unexpected column {column_name}"
            
            expected_type = expected_schema[column_name]['type']
            actual_type = str(column['type'])
            assert expected_type in actual_type, f"Expected type {expected_type} for column {column_name}, but got {actual_type}"
            
            """expected_nullable = expected_schema[column_name]['nullable']
            actual_nullable = column['nullable']
            assert expected_nullable == actual_nullable, f"Expected nullable={expected_nullable} for column {column_name}, but got nullable={actual_nullable}"

            expected_primary_key = expected_schema[column_name]['primary_key']
            actual_primary_key = column['primary_key']
            assert expected_primary_key == actual_primary_key, f"Expected primary_key={expected_primary_key} for column {column_name}, but got primary_key={actual_primary_key}"
            """



def test_postgre_database_exists():
    """ Checks that the Postgre database exists"""

    # Use SQL Alchemy engine
    engine, inspector = get_engine()
    
    expected_schema = {
        'genome_scores': ['movie_id', 'gtag_id', 'relevance', 'updated_at'],
        'genome_tags': ['gtag_id', 'tag', 'updated_at'],
        'links': ['movie_id', 'imdb_id', 'tmdb_id', 'updated_at'],
        'movies': ['movie_id', 'title', 'genres', 'updated_at'],
        'ratings': ['user_id', 'movie_id', 'rating', 'created_at', 'updated_at'],
        'tags': ['user_id', 'movie_id', 'tag', 'created_at', 'updated_at'],
        'users': ['user_id', 'user_key', 'updated_at'],
        #'predicted_ratings': ['pred_id', 'predicted_rating', 'model', 'feedback'],
        'recommendations': ['reco_id', 'movie_id', 'user_id', 'reco_type', 'reco_datetime', 'user_feedback']
    }

    actual_tables = inspector.get_table_names()
    expected_tables = list(expected_schema.keys())

    # Check if all expected tables are present
    assert(set(expected_tables).issubset(set(actual_tables))), f"Missing tables: {set(expected_tables) - set(actual_tables)}"
    
    # Check if there are any unexpected tables
    assert(set(actual_tables).issubset(set(expected_tables))), f"Unexpected tables: {set(actual_tables) - set(expected_tables)}"


def test_postgre_table_movie():
    """ Checks that movies table is correctly formatted and contained all expected fields """

    expected_schema = {
        'movie_id': {'type': 'INTEGER'},
        'title': {'type': 'VARCHAR(255)'},
        'genres': {'type': 'TEXT'},
        'updated_at': {'type': 'TIMESTAMP'}
    }

    check_table_details("movies", expected_schema)


def test_postgre_table_ratings():
    """ Checks that movies table is correctly formatted and contained all expected fields """

    expected_schema = {
        'user_id': {'type': 'INTEGER'},
        'movie_id': {'type': 'INTEGER'},
        'rating': {'type': 'NUMERIC(2, 1)'},
        'created_at': {'type': 'TIMESTAMP'},
        'updated_at': {'type': 'TIMESTAMP'}
    }

    check_table_details("ratings", expected_schema)


"""
def test_csv_database_exists():
    # Checks that the CSV database exists

    # Check whether the specified path exists or not
    files = ["movies.csv", "ratings.csv", "tags.csv", "genome-scores.csv", "genome-tags.csv"]

    for file in files:
        assert os.path.exists(os.path.join(path, file))

def test_csv_movies():
    # Checks that movies table is correctly formatted and contained all expected fields

    df = pd.read_csv(os.path.join(path, 'movies.csv'))

    # Check that the columns are correctly named and in the right order
    assert(df.columns.to_list() == ['movieId', 'title', 'genres'])

    # Check that the fields are correctly formatted
    assert(df['movieId'].dtypes == 'int64')
    assert(df['title'].dtypes == 'object')
    assert(df['genres'].dtypes == 'object')  

def test_csv_ratings():
    # Checks that ratings table is correctly formatted and contained all expected fields

    df = pd.read_csv(os.path.join(path, 'ratings.csv'))

    # Check that the columns are correctly named and in the right order
    assert(df.columns.to_list() == ['userId', 'movieId', 'rating', 'timestamp'])

    # Check that the fields are correctly formatted
    assert(df['userId'].dtypes == 'int64')
    assert(df['movieId'].dtypes == 'int64')
    assert(df['rating'].dtypes == 'float64')
    assert(df['timestamp'].dtypes == 'int64')

    # Check that rating are between 0.5 and 5, and only in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    assert(sorted(list(set(df['rating'].values))) == [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])

    # Check timestamp between 1/1/95 and now
    assert(df['timestamp'].min() >= min_expected_ts)
    assert(df['timestamp'].max() <= current_ts)



def test_csv_tags():
    # Checks that tags table is correctly formatted and contained all expected fields

    df = pd.read_csv(os.path.join(path, 'tags.csv'))

    # Check that the columns are correctly named and in the right order
    assert(df.columns.to_list() == ['userId', 'movieId', 'tag', 'timestamp'])

    # Check that the fields are correctly formatted
    assert(df['userId'].dtypes == 'int64')
    assert(df['movieId'].dtypes == 'int64')
    assert(df['tag'].dtypes == 'object')
    assert(df['timestamp'].dtypes == 'int64')

    # Check timestamp between 1/1/95 and now
    assert(df['timestamp'].min() >= min_expected_ts)
    assert(df['timestamp'].max() <= current_ts)


def test_csv_genome_scores():
    # Checks that tags table is correctly formatted and contained all expected fields

    df = pd.read_csv(os.path.join(path, 'genome-scores.csv'))

    # Check that the columns are correctly named and in the right order
    assert(df.columns.to_list() == ['movieId', 'tagId', 'relevance'])

    # Check that the fields are correctly formatted
    assert(df['movieId'].dtypes == 'int64')
    assert(df['tagId'].dtypes == 'int64')
    assert(df['relevance'].dtypes == 'float64')


def test_csv_genome_tags():
    # Checks that tags table is correctly formatted and contained all expected fields

    df = pd.read_csv(os.path.join(path, 'genome-tags.csv'))

    # Check that the columns are correctly named and in the right order
    assert(df.columns.to_list() == ['tagId', 'tag'])

    # Check that the fields are correctly formatted
    assert(df['tagId'].dtypes == 'int64')
    assert(df['tag'].dtypes == 'object')
"""
