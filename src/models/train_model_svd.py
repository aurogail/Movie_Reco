import pandas as pd
from surprise import SVD
from surprise.model_selection import cross_validate
import pickle
import sys
sys.path.append('src')
from src.models.load_svd_data import load_and_prepare_data

def evaluate_svd_model(measures=['RMSE', 'MAE'], cv=5):

    df_surprise,_ = load_and_prepare_data()
    svd = SVD()
    cv_results = cross_validate(svd, df_surprise, measures=measures, cv=cv, verbose=True )
    return svd, cv_results

def train_svd_model():

    _, train_set = load_and_prepare_data()
    svd_model = SVD().fit(train_set)
    filehandler = open("src/models/svd_model.pkl", "wb")
    pickle.dump(svd_model, filehandler)
    filehandler.close()
    return svd_model

def load_svd_model():
    with open("src/models/svd_model.pkl", "rb") as filehandler:
        return pickle.load(filehandler)

if __name__ == "__main__":
    #svd, cv_results = evaluate_svd_model(df_surprise)
    svd_model = train_svd_model()

    filehandler = open("src/models/svd_model.pkl", "wb")
    pickle.dump(svd_model, filehandler)
    filehandler.close()

    #print("Résultats de la validation croisée :")
    #print(cv_results)
    print("Le modèle SVD a été entraîné et sauvegardé avec succès.")

