import pandas as pd
import pickle
from surprise import Reader, Dataset, SVD
from train_model_svd import train_svd_model

def collab_reco(user_id, num_recommendations=10):

    anti_testset = []
    df_ratings = pd.read_csv("../data/raw/ratings.csv")
    df_ratings = df_ratings.drop("timestamp", axis=1)
    reader = Reader(rating_scale=(0, 5))
    df_surprise = Dataset.load_from_df(df_ratings, reader=reader)
    train_set = df_surprise.build_full_trainset()
    targetUser = train_set.to_inner_uid(user_id)
    moyenne = train_set.global_mean
    user_note = train_set.ur[targetUser]
    user_film = [item for (item, _) in user_note]

    for film in train_set.all_items():
        if film not in user_film:
            anti_testset.append((user_id, train_set.to_raw_iid(film), moyenne))

    filehandler = open("svd_model.pkl", "rb")
    svd_model = pickle.load(filehandler)
    filehandler.close()

    predictionsSVD = svd_model.test(anti_testset)
    predictionsSVD = pd.DataFrame(predictionsSVD)

    df_movies = pd.read_csv("../data/raw/movies.csv")
    movieId_title_map = df_movies.set_index('movieId')['title'].to_dict()
    predictionsSVD['title'] = predictionsSVD['iid'].map(movieId_title_map)

    predictionsSVD = predictionsSVD.rename(columns={'uid': 'userId', 'est': 'note'})
    predictionsSVD = predictionsSVD[['userId', 'title', 'note']]
    predictionsSVD.sort_values('note', ascending=False, inplace=True)

    return predictionsSVD.head(num_recommendations)

if __name__ == "__main__":

    user_id = 1000
    recommendations = collab_reco(user_id)
    print(recommendations)
