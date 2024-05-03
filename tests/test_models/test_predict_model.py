#import sys
#sys.path.append('src')

from models.predict_model import make_predictions

def test_number_predictions():
    """ Checks that the model returns 10 predictions"""

    users_id = [1, 2]
    matrix = make_predictions(users_id, "models/model.pkl", "tests/fixtures/user_matrix_test.csv")

    assert matrix.shape == (2, 10)