import pytest
from src.models.train_model_svd import load_svd_model
from src.models.hybrid_predict import hybride_reco

@pytest.fixture(scope="module")
def svd_model_fixture():
    return load_svd_model()

def test_hybride_reco(svd_model_fixture):
    user_id = 1000
    titre = "Toy Story (1995)"  
    num_recommendations = 10
    alpha = 0.8
    n = 1000

    try:
        recommendations = hybride_reco(user_id, svd_model_fixture, titre, 
num_recommendations, alpha, n)

        assert recommendations is not None
        assert not recommendations.empty  
        expected_columns = ['title', 'score_content', 'score_collab', 'score']
        assert all(col in recommendations.columns for col in expected_columns)
        assert len(recommendations) == num_recommendations

    except Exception as e:
        pytest.fail(f"Error encountered while calling hybride_reco: {e}")
