import pandas as pd
import os
import sys
sys.path.append('src')
from surprise import Reader, Dataset
from joblib import Memory

cachedir = 'cache'
os.makedirs(cachedir, exist_ok=True)
memory = Memory(cachedir, verbose=True)

@memory.cache
def load_and_prepare_data(ratings_path="src/data/raw/ratings.csv", rating_scale=(0, 5)):
    """
    Description:
    This function loads user ratings data from a CSV file, prepares it for use with the Surprise library,
    and builds a full training set for collaborative filtering.

    Args:
    - ratings_path (str): The file path to the CSV file containing the ratings data. Defaults to "src/data/raw/ratings.csv".
    - rating_scale (tuple): A tuple specifying the rating scale. Defaults to (0, 5).

    Returns:
    - surprise.dataset.DatasetAutoFolds: The loaded ratings dataset in a format suitable for the Surprise library.
    - surprise.Trainset: The full training set built from the ratings data.
    """
    
    df_ratings = pd.read_csv(ratings_path)
    df_ratings = df_ratings.drop("timestamp", axis=1)
    reader = Reader(rating_scale=rating_scale)
    df_surprise = Dataset.load_from_df(df_ratings, reader=reader)
    train_set = df_surprise.build_full_trainset()
    return df_surprise, train_set

if __name__ == "__main__":
    df_surprise, train_set = load_and_prepare_data()