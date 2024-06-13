import pytest
import pandas as pd
import scipy as sp
from src.features.build_tfidf_matrix import calculer_matrice_tfidf


@pytest.fixture
def mock_df():
    # Créer un DataFrame avec les données d'échantillon
    data = {
        'movieId': [1, 2, 3, 4, 5],
        'title': ['Toy Story (1995)', 'Jumanji (1995)', 'Grumpier Old Men (1995)', 'Waiting to Exhale (1995)', 'Father of the Bride Part II (1995)'],
        'all_tags': [
            "pixar, innovative, fun, animated, cgi, cartoon, dvd-video, family, disney, usa, dolls, friendship, comedy, humorous, animation, want, fantasy, witty, children, warm, bd-video, clv, buy, woody, light, engaging, adventure, funny, rated-g, cute, classic, rousing, toys, avi, soothing, clever, fanciful, watched, toy, bright, story",
            "jungle, children, lebbat, childish, clv, game, time, monkey, fantasy, animals, adventure, scary",
            "romance, comedy, moldy, clv, sequels, sequel, old",
            "romance, characters, women, comedy, revenge, clv, drama",
            "pregnancy, remake, comedy, clv, fantasy, touching, sequels, sequel, family, wedding"
        ]
    }
    return pd.DataFrame(data)


# Test de la fonction calculer_matrice_tfidf
def test_calculer_matrice_tfidf(mock_df):
    # Appeler la fonction sur les données d'échantillon
    tfidf_matrix = calculer_matrice_tfidf(mock_df)

    # Vérifier que la matrice retournée est bien une matrice sparse
    assert isinstance(tfidf_matrix, sp.sparse.spmatrix)

    # Vérifier que la matrice n'est pas vide
    assert tfidf_matrix.nnz > 0


if __name__ == "__main__":
    pytest.main([__file__])

