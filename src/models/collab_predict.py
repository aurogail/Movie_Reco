import pandas as pd
import sys
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

    print("Step 1")

    # List to store items not rated by the user
    anti_testset =[]
    # Load and prepare the data
    #_, train_set = load_and_prepare_data()
    _, train_set = load_and_prepare_data_from_db()

    print("Step 2")

    # Convert the user ID to the internal ID used by the training set
    target_user = train_set.to_inner_uid(user_id)
    # Get the global mean rating
    moyenne = train_set.global_mean
    # Get the movies rated by the user
    user_note = train_set.ur[target_user]
    user_film = [item for (item, _) in user_note]

    print("Step 3")

    # Create the anti-test set with movies the user has not rated
    for film in train_set.all_items():
        if film not in user_film:
            anti_testset.append((user_id, train_set.to_raw_iid(film), moyenne))

    print("Step 4")

    # Generate predictions using the SVD model
    predictions_svd = svd_model.test(anti_testset)
    predictions_svd = pd.DataFrame(predictions_svd)

    # Load movie data to map movie IDs to titles
    # df_movies = pd.read_csv("src/data/raw/movies.csv")
    # movieId_title_map = df_movies.set_index('movieId')['title'].to_dict()

    print("Step 5")

    # Use SQL Alchemy engine
    engine, inspector = get_engine()

    query = "SELECT * FROM movies;"
    df_movies = pd.read_sql(query, engine)
    movieId_title_map = df_movies.set_index('movie_id')['title'].to_dict()

    print("Step 6")

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

    svd_model = load_svd_model()
    print("model loaded")
    
    # test of generate_new_recommendtaions
    user_id = 1000
    recommendations = collab_reco(user_id, svd_model)
    print(recommendations)
    satisfaction = input("Êtes-vous satisfait de ces recommandations ? (Oui/Non): ")

    if satisfaction.lower() == "non":
        new_recommendations = generate_new_recommendations(recommendations)
        print(new_recommendations)
        