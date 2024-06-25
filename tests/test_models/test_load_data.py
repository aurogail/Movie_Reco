import os
import sys
import pytest
import pandas as pd
from src.models.load_svd_data import load_and_prepare_data, load_and_prepare_data_from_db
sys.path.append('src')


@pytest.fixture
def ratings_path():
    return "src/data/raw/ratings.csv"
"""
def test_load_and_prepare_data(ratings_path):
    start_time = pd.Timestamp.now()
    df_surprise, train_set = load_and_prepare_data(ratings_path)
    end_time = pd.Timestamp.now()
    execution_time = (end_time - start_time).total_seconds()
    
    # Vérification que les données ont été chargées correctement
    assert df_surprise is not None
    assert train_set is not None
    
    # Vérification que le train_set est non vide
    assert len(train_set.all_users()) > 0
    assert len(train_set.all_items()) > 0
    
    # Vérification que les données sont cohérentes avec les ratings
    assert len(df_surprise.raw_ratings) == train_set.n_ratings

    # Affichage du temps d'exécution
    print(f"Temps d'exécution : {execution_time} secondes")"""

def test_load_and_prepare_data_from_db():
    start_time = pd.Timestamp.now()
    df_surprise, train_set = load_and_prepare_data_from_db()
    end_time = pd.Timestamp.now()
    execution_time = (end_time - start_time).total_seconds()
    
    # Vérification que les données ont été chargées correctement
    assert df_surprise is not None
    assert train_set is not None
    
    # Vérification que le train_set est non vide
    assert len(train_set.all_users()) > 0
    assert len(train_set.all_items()) > 0
    
    # Vérification que les données sont cohérentes avec les ratings
    assert len(df_surprise.raw_ratings) == train_set.n_ratings

    # Affichage du temps d'exécution
    print(f"Temps d'exécution : {execution_time} secondes")



if __name__ == "__main__":
    pytest.main([__file__])

