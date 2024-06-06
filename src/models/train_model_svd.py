import pandas as pd
from surprise import SVD
from surprise.model_selection import cross_validate
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

    load_data_time = time.time()
    elapsed_time = load_data_time - start_time
    print("Loading data took: ", round(elapsed_time, 4), "seconds")

    # Train SVD Model
    svd_model = SVD().fit(train_set)

    training_svd_time = time.time()
    elapsed_time = training_svd_time - load_data_time
    print("Training data took: ", round(elapsed_time, 4), "seconds")

    # Saving Model
    filehandler = open("src/models/svd_model.pkl", "wb")
    pickle.dump(svd_model, filehandler)
    filehandler.close()

    saving_model_time = time.time()
    elapsed_time = saving_model_time - training_svd_time
    print("Saving model took: ", round(elapsed_time, 4), "seconds")

    return svd_model

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
    #svd, cv_results = evaluate_svd_model()
    svd_model = train_svd_model()
    # filehandler = open("src/models/svd_model.pkl", "wb")
    # pickle.dump(svd_model, filehandler)
    # filehandler.close()

    #print("Résultats de la validation croisée :")
    #print(cv_results)
    print("Le modèle SVD a été entraîné et sauvegardé avec succès.")

