import sys
sys.path.append('src')

from models.predict_model import make_predictions

def test_number_predictions():

    users_id = [1, 2]
    matrix = make_predictions(users_id, "src/models/model.pkl", "tests/fixtures/user_matrix_test.csv")

    assert matrix.shape == (2, 10)

# def test_user_not_exists():

#     users_id = [0]
#     matrix = make_predictions(users_id, "src/models/model.pkl", "src/data/processed/user_matrix.csv")

#     assert matrix.shape == (0, 5)