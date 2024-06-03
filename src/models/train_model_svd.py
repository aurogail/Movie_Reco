import pandas as pd
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
import pickle

def evaluate_svd_model(data, measures=['RMSE', 'MAE'], cv=5):

    reader = Reader(rating_scale=(0, 5))
    df_surprise = Dataset.load_from_df(data, reader=reader)
    svd = SVD()
    cv_results = cross_validate(svd, df_surprise,measures=measures, cv=cv, verbose=True )
    return svd, df_surprise, cv_results

def train_svd_model(svd, df_surprise):

    train_set = df_surprise.build_full_trainset()
    svd.fit(train_set)
    return svd, train_set

if __name__ == "__main__":
    # Chemins vers les fichiers de données
    df_ratings = pd.read_csv("../data/raw/ratings.csv")
    df_ratings = df_ratings.drop("timestamp", axis=1)

    svd, df_surprise, cv_results = evaluate_svd_model(df_ratings)
    svd_model = train_svd_model(svd, df_surprise)

    # Entraîner le modèle SVD
    model_path = "../models/svd_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(svd_model, f)

    print("Résultats de la validation croisée :")
    print(cv_results)
    print("Le modèle SVD a été entraîné et sauvegardé avec succès.")