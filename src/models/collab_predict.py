import pandas as pd
import sys
import time
sys.path.append('src')
from src.models.train_model_svd import load_svd_model
from src.models.load_svd_data import load_and_prepare_data_from_db
from src.data.db.database_functions import get_engine

def collab_reco(user_id, svd_model, num_recommendations=10, start_index=0):
    """
    Description:
    This function generates collaborative movie recommendations for a given user using the provided SVD model.

    Args:
    - user_id (str): The ID of the user for whom recommendations are generated.
    - svd_model (Surprise SVD model): The trained SVD model used for generating recommendations.
    - num_recommendations (int): The number of recommendations to generate. Defaults to 10.
    - start_index (int): The starting index for recommendations, useful for printing the next movies. Defaults to 0.

    Returns:
    - DataFrame: A DataFrame containing the recommended movie titles and their estimated ratings.
    """

    # Use SQL Alchemy engine
    engine, inspector = get_engine()

    # Generate a list of movies unrated by the user
    query = f"""WITH movies_rated AS (SELECT DISTINCT(movie_id) FROM ratings WHERE user_id={user_id} ORDER BY movie_id)
    SELECT movie_id                                                                                    
    FROM movies                                                                                        
    WHERE movie_id NOT IN (SELECT movie_id FROM movies_rated);"""

    unrated_movies = pd.read_sql(query, engine)
    unrated_movies_list = unrated_movies['movie_id'].to_list()

    avg_rating = 3.525529
    anti_testset = [(user_id, movie_id, avg_rating) for movie_id in unrated_movies_list]

    # Generate predictions using the SVD model
    predictions_svd = svd_model.test(anti_testset)
    predictions_svd = pd.DataFrame(predictions_svd)

    # Get the titles of the movies
    query = "SELECT * FROM movies;"
    df_movies = pd.read_sql(query, engine)
    movieId_title_map = df_movies.set_index('movie_id')['title'].to_dict()
    predictions_svd['title'] = predictions_svd['iid'].map(movieId_title_map)

    # Rename and reorder the columns for clarity
    predictions_svd = predictions_svd.rename(columns={'uid': 'userId', 'est': 'note'})
    predictions_svd = predictions_svd[['userId', 'title', 'note']]

    # Sort the predictions by rating in descending order
    predictions_svd.sort_values('note', ascending=False, inplace=True)

    return predictions_svd.iloc[start_index:start_index + num_recommendations]


def generate_new_recommendations(top_recommendations_collab):
    """
    Description:
    This function generates a new set of collaborative movie recommendations based on the length of previously generated recommendations.

    Args:
    - top_recommendations_collab (DataFrame): The DataFrame containing the current top collaborative recommendations.

    Returns:
    - DataFrame: A DataFrame containing the new set of recommended movie titles and their estimated ratings.
    """

    start_index = len(top_recommendations_collab)
    new_recommendations = collab_reco(user_id, start_index, num_recommendations=10)
    
    return new_recommendations


if __name__ == "__main__":

    # Start timer
    start_time = time.time()

    svd_model = load_svd_model()
    print("model loaded")
    loading_model_time = time.time()
    elapsed_time = loading_model_time - start_time
    print("Loading model took: ", round(elapsed_time, 4), "seconds")

    # test of generate_new_recommendtaions
    user_id = 1000
    recommendations = collab_reco(user_id, svd_model)

    reco_predict_time = time.time()
    elapsed_time = reco_predict_time - loading_model_time
    print("Running recommendations took: ", round(elapsed_time, 4), "seconds")

    print(recommendations)
    satisfaction = input("Êtes-vous satisfait de ces recommandations ? (Oui/Non): ")

    if satisfaction.lower() == "non":
        new_recommendations = generate_new_recommendations(recommendations)
        print(new_recommendations)
        