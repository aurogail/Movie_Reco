import pandas as pd
import os
import mlflow
import sys
sys.path.append('src')
from src.models.train_model_svd import *
from src.models.load_svd_data import *

memory = Memory(cachedir, verbose=True)
# Define experiment name

def collab_reco(user_id, svd_model, train_set, num_recommendations=10):
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

    # Check if temporary directory exist otherwise it's created
    temp_dir = "src/models/temp/"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # MLflow experiment
    experiment_name = "SVD_Collab_Pred"
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="collab_reco"):
        # List to store items not rated by the user
        anti_testset =[]
        # Convert the user ID to the internal ID used by the training set
        target_user = train_set.to_inner_uid(user_id)
        # Get the global mean rating
        moyenne = train_set.global_mean
        # Get the movies rated by the user
        user_note = train_set.ur[target_user]
        user_film = [item for (item, _) in user_note]

        # Create the anti-test set with movies the user has not rated
        for film in train_set.all_items():
            if film not in user_film:
                anti_testset.append((user_id, train_set.to_raw_iid(film), moyenne))

        # Generate predictions using the SVD model
        predictions_svd = svd_model.test(anti_testset)
        predictions_svd = pd.DataFrame(predictions_svd)

        # Load movie data to map movie IDs to titles
        df_movies = pd.read_csv("src/data/raw/movies.csv")
        movieId_title_map = df_movies.set_index('movieId')['title'].to_dict()
        predictions_svd['title'] = predictions_svd['iid'].map(movieId_title_map)

        # Rename and reorder the columns for clarity
        predictions_svd = predictions_svd.rename(columns={'uid': 'userId', 'est': 'note'})
        predictions_svd = predictions_svd[['userId', 'title', 'note']]
        # Sort the predictions by rating in descending order
        predictions_svd.sort_values('note', ascending=False, inplace=True)

        # Enregistrer le fichier CSV localement
        collab_pred_path = os.path.join(temp_dir, "collab_pred.csv")
        predictions_svd.head(num_recommendations).to_csv(collab_pred_path, index=False)

        # Log predictions
        mlflow.log_param("user_id", user_id)
        mlflow.log_param("num_recommendations", num_recommendations)
        mlflow.log_artifact(collab_pred_path)

    return predictions_svd.head(num_recommendations)

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
    df_surprise, train_set = load_and_prepare_data()
    user_id = 1000
    recommendations = collab_reco(user_id, svd_model, train_set)
    print(recommendations)
    satisfaction = input("Êtes-vous satisfait de ces recommandations ? (Oui/Non): ")

    if satisfaction.lower() == "non":
        new_recommendations = generate_new_recommendations(recommendations)
        print(new_recommendations)
