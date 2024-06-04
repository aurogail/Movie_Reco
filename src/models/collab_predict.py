import pandas as pd
import pickle
import sys
sys.path.append('src')
from src.models.train_model_svd import *
from src.models.load_svd_data import *

def collab_reco(user_id, svd_model, num_recommendations=10):

    anti_testset =[]
    _, train_set = load_and_prepare_data()
    target_user = train_set.to_inner_uid(user_id)
    moyenne = train_set.global_mean
    user_note = train_set.ur[target_user]
    user_film = [item for (item, _) in user_note]

    for film in train_set.all_items():
        if film not in user_film:
            anti_testset.append((user_id, train_set.to_raw_iid(film), moyenne))

    predictions_svd = svd_model.test(anti_testset)
    predictions_svd = pd.DataFrame(predictions_svd)

    df_movies = pd.read_csv("src/data/raw/movies.csv")
    movieId_title_map = df_movies.set_index('movieId')['title'].to_dict()
    predictions_svd['title'] = predictions_svd['iid'].map(movieId_title_map)

    predictions_svd = predictions_svd.rename(columns={'uid': 'userId', 'est': 'note'})
    predictions_svd = predictions_svd[['userId', 'title', 'note']]
    predictions_svd.sort_values('note', ascending=False, inplace=True)

    return predictions_svd.head(num_recommendations)

if __name__ == "__main__":

    svd_model = load_svd_model()
    
    user_id = 1000
    recommendations = collab_reco(user_id, svd_model)
    print(recommendations)
    user_id = 123
    recommendations = collab_reco(user_id, svd_model)
    print(recommendations)
