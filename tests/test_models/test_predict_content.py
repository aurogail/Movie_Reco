import pytest
from src.models.content_predict import content_based_reco


def test_content_based_reco():

    titre = "Toy Story (1995)"
    num_recommendations = 10

    try:

        recommendations = content_based_reco(titre, num_recommendations)
        assert recommendations is not None
        assert not recommendations.empty  

        expected_columns = ['title', 'score']
        assert all(col in recommendations.columns for col in expected_columns)
        assert len(recommendations) == num_recommendations

    except Exception as e:
        pytest.fail(f"Erreur lors de l'appel à content_based_reco : {e}")

