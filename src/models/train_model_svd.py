import pandas as pd
from surprise import SVD
from surprise.model_selection import cross_validate
import logging
import pickle
import time
import sys
sys.path.append('src')
from src.models.load_svd_data import load_and_prepare_data, load_and_prepare_data_from_db

def evaluate_svd_model(measures=['RMSE', 'MAE'], cv=5):
    """
    Description:
    This function evaluates an SVD model using cross-validation on the provided dataset. 
    It calculates specified performance measures and returns the trained SVD model along with the cross-validation results.

    Args:
    - measures (list): A list of performance measures to evaluate. Defaults to ['RMSE', 'MAE'].
    - cv (int): The number of cross-validation folds. Defaults to 5.

    Returns:
    - SVD: The trained SVD model.
    - dict: A dictionary containing cross-validation results.
    """

    # df_surprise,_ = load_and_prepare_data()
    df_surprise,_ = load_and_prepare_data_from_db()
    svd = SVD()
    cv_results = cross_validate(svd, df_surprise, measures=measures, cv=cv, verbose=True )
    return svd, cv_results

def train_svd_model():

    #logger = logging.getLogger("airflow.task")
    logger = logging.getLogger(__name__)
    
    """
    Description:
    This function trains an SVD model on the provided dataset and saves the trained model to a pickle file. 
    It returns the trained SVD model.

    Args:
    None

    Returns:
    - SVD: The trained SVD model.
    """

    # Start timer
    start_time = time.time()

    # Load and Prepare Data
    # _, train_set = load_and_prepare_data()
    _, train_set = load_and_prepare_data_from_db()

    # Saving inner IDs and average rating of the model
    # Convert the user ID to the internal ID used by the training set
    #target_user = train_set.to_inner_uid(user_id)
    # Get the global mean rating
    moyenne = train_set.global_mean

    print(moyenne)
    logger.info(moyenne)

    # Create the mapping from raw user IDs to inner user IDs
    raw_to_inner_uid_mapping = {train_set.to_raw_uid(inner_uid): inner_uid for inner_uid in train_set.all_users()}

    # Print the mappings
    print("\nRaw to Inner User ID Mapping:")
    for raw_uid, inner_uid in raw_to_inner_uid_mapping.items():
        print(f"Raw User ID: {raw_uid}, Inner User ID: {inner_uid}")

    # Create the mapping from raw movie IDs to inner movie IDs
    raw_to_inner_iid_mapping = {train_set.to_raw_iid(inner_iid): inner_iid for inner_iid in train_set.all_items()}

    # Print the mappings
    print("\nRaw to Inner Item ID Mapping:")
    for raw_iid, inner_iid in raw_to_inner_iid_mapping.items():
        print(f"Raw Item ID: {raw_iid}, Inner Item ID: {inner_iid}")

    user_id_mapping = pd.DataFrame(list(raw_to_inner_uid_mapping.items()), columns=['Raw User ID', 'Inner User ID'])
    user_id_mapping.to_csv('src/models/user_id_mapping.csv', index = None)

    item_id_mapping = pd.DataFrame(list(raw_to_inner_iid_mapping.items()), columns=['Raw Item ID', 'Inner Item ID'])
    item_id_mapping.to_csv('src/models/item_id_mapping.csv', index = None)

    load_data_time = time.time()
    elapsed_time = load_data_time - start_time
    print("Loading data took: ", round(elapsed_time, 4), "seconds")
    logger.info(f"Loading data took: {round(elapsed_time, 4)} seconds")

    # Train SVD Model
    svd_model = SVD().fit(train_set)

    training_svd_time = time.time()
    elapsed_time = training_svd_time - load_data_time
    print("Training data took: ", round(elapsed_time, 4), "seconds")
    logger.info(f"Training data took: {round(elapsed_time, 4)} seconds")

    # Saving Model
    filehandler = open("src/models/svd_model.pkl", "wb")
    pickle.dump(svd_model, filehandler)
    filehandler.close()

    saving_model_time = time.time()
    elapsed_time = saving_model_time - training_svd_time
    print(f"Saving model took: ", round(elapsed_time, 4), "seconds")
    logger.info(f"Saving model took: {round(elapsed_time, 4)} seconds")



    # return svd_model

def load_svd_model():
    """
    Description:
    This function loads a previously trained SVD model from a file and returns it.

    Args:
    None

    Returns:
    - SVD: The loaded SVD model.
    """
    
    with open("src/models/svd_model.pkl", "rb") as filehandler:
        return pickle.load(filehandler)

if __name__ == "__main__":

    try:
        svd_model = train_svd_model()
        print("Le modèle SVD a été entraîné et sauvegardé avec succès.")
    
    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception to mark the task as failed
        
    #svd, cv_results = evaluate_svd_model()
    # filehandler = open("src/models/svd_model.pkl", "wb")
    # pickle.dump(svd_model, filehandler)
    # filehandler.close()

    #print("Résultats de la validation croisée :")
    #print(cv_results)
    
