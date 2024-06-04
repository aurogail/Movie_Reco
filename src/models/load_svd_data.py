import pandas as pd
from surprise import Reader, Dataset

def load_and_prepare_data(ratings_path="../data/raw/ratings.csv", rating_scale=(0, 5)):
    df_ratings = pd.read_csv(ratings_path)
    df_ratings = df_ratings.drop("timestamp", axis=1)
    reader = Reader(rating_scale=rating_scale)
    df_surprise = Dataset.load_from_df(df_ratings, reader=reader)
    train_set = df_surprise.build_full_trainset()
    return df_surprise, train_set

