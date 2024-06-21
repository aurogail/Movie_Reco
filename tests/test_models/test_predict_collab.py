import pytest
from src.models.train_model_svd import load_svd_model
from src.models.collab_predict import collab_reco

@pytest.fixture(scope="module")
def svd_model_fixture():
    return load_svd_model()

def test_collab_reco(svd_model_fixture):
    user_id = 1000
    svd_model = svd_model_fixture  

    try:
        recommendations = collab_reco(user_id, svd_model)
        assert recommendations is not None
        assert not recommendations.empty  
        expected_columns = ['userId', 'title', 'note']
        assert all(col in recommendations.columns for col in expected_columns)
        assert len(recommendations) == 10   
    except Exception as e:
        pytest.fail(f"Erreur lors de l'appel à collab_reco : {e}")
