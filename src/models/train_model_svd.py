import pandas as pd
from surprise import SVD
import mlflow
import mlflow.sklearn
from surprise.model_selection import cross_validate
import pickle
import numpy as np
from joblib import Memory
import os
import sys
sys.path.append('src')
from src.models.load_svd_data import load_and_prepare_data

cachedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cache'))
os.makedirs(cachedir, exist_ok=True)
memory = Memory(cachedir, verbose=True)
'''
# Define experiment name
experiment_name = "SVD_Movie_Reco"
mlflow.set_experiment(experiment_name)
'''

def evaluate_svd_model(measures=['rmse', 'mae'], cv=5):

    df_surprise,_ = load_and_prepare_data()
    svd = SVD(n_factors=100, n_epochs=30, lr_all=0.01, reg_all=0.05)

    with mlflow.start_run(run_name="evaluation"):
        cv_results = cross_validate(svd, df_surprise, measures=measures, cv=cv, verbose=True)
        # Log metrics for each measure
        for metric in measures:
            mean_metric = cv_results[f'test_{metric}'].mean()
            std_metric = cv_results[f'test_{metric}'].std()
            mlflow.log_metric(f'{metric}_mean', mean_metric)
            mlflow.log_metric(f'{metric}_std', std_metric)
        
        # Log the training and testing times
        mlflow.log_metric('fit_time_mean', np.mean(cv_results['fit_time']))
        mlflow.log_metric('fit_time_std', np.std(cv_results['fit_time']))
        mlflow.log_metric('test_time_mean', np.mean(cv_results['test_time']))
        mlflow.log_metric('test_time_std', np.std(cv_results['test_time']))

        mlflow.log_params({"n_factors": 100, "n_epochs": 30, "lr_all": 0.01, "reg_all": 0.05})
        mlflow.log_params({"measures": measures, "cv": cv})
    return svd, cv_results


@memory.cache
def train_svd_model():

    _, train_set = load_and_prepare_data()
    svd_model = SVD(n_factors=100, n_epochs=30, lr_all=0.01, reg_all=0.05).fit(train_set)
    model_path = "src/models/svd_model.pkl"
    with open(model_path, "wb") as filehandler:
        pickle.dump(svd_model, filehandler)

    # Enregistrer le modèle entraîné et l'artefact
    with mlflow.start_run(run_name="training"):
        mlflow.log_params({"n_factors": 100, "n_epochs": 30, "lr_all": 0.01, "reg_all": 0.05})
        mlflow.sklearn.log_model(svd_model, "svd_model")
        mlflow.log_artifact(model_path)
    return svd_model

@memory.cache
def load_svd_model(filepath="src/models/svd_model.pkl"):
    with open(filepath, "rb") as filehandler:
        return pickle.load(filehandler)

if __name__ == "__main__":
    #svd, cv_results = evaluate_svd_model()
    svd_model = train_svd_model()

    #print("Résultats de la validation croisée :")
    #print(cv_results)
    print("Le modèle SVD a été entraîné et sauvegardé avec succès.")


