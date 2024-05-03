import os
import pandas as pd
from datetime import datetime

path = "src/data/raw"
current_time = datetime.now()
current_ts = current_time.timestamp()
min_expected_ts = datetime(1995, 1, 1, 0, 0, 0).timestamp()           # we don't expect data prior to 1995


def test_database_exists():
    """ Checks that the database exists"""

    # Check whether the specified path exists or not
    files = ["movies.csv", "ratings.csv", "tags.csv", "genome-scores.csv", "genome-tags.csv"]

    for file in files:
        assert os.path.exists(os.path.join(path, file))


def test_movies():
    """ Checks that movies table is correctly formatted and contained all expected fields"""

    df = pd.read_csv(os.path.join(path, 'movies.csv'))

    # Check that the columns are correctly named and in the right order
    assert(df.columns.to_list() == ['movieId', 'title', 'genres'])

    # Check that the fields are correctly formatted
    assert(df['movieId'].dtypes == 'int64')
    assert(df['title'].dtypes == 'object')
    assert(df['genres'].dtypes == 'object')    


def test_ratings():
    """ Checks that ratings table is correctly formatted and contained all expected fields"""

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


datetime(1995, 1, 1, 0, 0, 0).timestamp()

def test_tags():
    """ Checks that tags table is correctly formatted and contained all expected fields"""

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


def test_genome_scores():
    """ Checks that tags table is correctly formatted and contained all expected fields"""

    df = pd.read_csv(os.path.join(path, 'genome-scores.csv'))

    # Check that the columns are correctly named and in the right order
    assert(df.columns.to_list() == ['movieId', 'tagId', 'relevance'])

    # Check that the fields are correctly formatted
    assert(df['movieId'].dtypes == 'int64')
    assert(df['tagId'].dtypes == 'int64')
    assert(df['relevance'].dtypes == 'float64')


def test_genome_tags():
    """ Checks that tags table is correctly formatted and contained all expected fields"""

    df = pd.read_csv(os.path.join(path, 'genome-tags.csv'))

    # Check that the columns are correctly named and in the right order
    assert(df.columns.to_list() == ['tagId', 'tag'])

    # Check that the fields are correctly formatted
    assert(df['tagId'].dtypes == 'int64')
    assert(df['tag'].dtypes == 'object')