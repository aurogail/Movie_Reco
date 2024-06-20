import pytest
from surprise import SVD
from src.models.train_model_svd import evaluate_svd_model, train_svd_model, load_svd_model
import os

# Définir un dossier de test pour les artefacts de MLflow
TEST_ARTIFACTS_DIR = "test_artifacts"

@pytest.fixture(scope="session")
def cleanup():
    """
    Fixture pour nettoyer les artefacts de MLflow après les tests.
    """
    yield
    if os.path.exists(TEST_ARTIFACTS_DIR):
        os.system(f"rm -r {TEST_ARTIFACTS_DIR}")

# Test de la fonction load_svd_model
def test_load_svd_model():
    svd_model = load_svd_model()

    # Vérifier que le modèle chargé est un objet SVD
    assert isinstance(svd_model, type(SVD()))

# Test de la fonction evaluate_svd_model
def test_evaluate_svd_model(cleanup):
    svd_model, cv_results = evaluate_svd_model()
    
    # Vérifier que le modèle retourné est un objet SVD
    assert isinstance(svd_model, type(SVD()))

    # Vérifier que les résultats de la validation croisée ne sont pas vides
    assert cv_results is not None

    # Vérifier que les artefacts de MLflow ont été enregistrés
    assert os.path.exists(f"{TEST_ARTIFACTS_DIR}/evaluation")

# Test de la fonction train_svd_model
def test_train_svd_model(cleanup):
    svd_model = train_svd_model()

    # Vérifier que le modèle retourné est un objet SVD
    assert isinstance(svd_model, type(SVD()))

    # Vérifier que le modèle entraîné a été sauvegardé
    assert os.path.exists("src/models/svd_model.pkl")

    # Vérifier que les artefacts de MLflow ont été enregistrés
    assert os.path.exists(f"{TEST_ARTIFACTS_DIR}/training")



if __name__ == "__main__":
    pytest.main([__file__])

