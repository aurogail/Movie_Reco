import sys
import pandas as pd
from pandas.testing import assert_frame_equal
sys.path.append('src')

from features.build_features import read_movies, create_user_matrix


def test_create_user_matrix():
    """ Checks that the user matrix is correctly created based on ratings and movies"""

    movies = pd.DataFrame({
        'movieId': [1, 2, 3, 4, 5],
        'title': ['Toy Story (1995)', 'Jumanji (1995)', 'Grumpier Old Men (1995)', 'Waiting to Exhale (1995)', 'Father of the Bride Part II (1995)'],
        'Action': [0, 0, 0, 0, 0],
        'Adventure': [1, 1, 0, 0, 0]
    })

    ratings = pd.DataFrame({
        'userId': [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        'movieId': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        'rating': [1.0, 2.0, 3.0, 4.0, 5.0, 5.0, 4.0, 3.0, 2.0, 1.0],
        'timestamp': [1112486027, 1112486028, 1112486029, 1112486030, 1112486031, 1112486032, 1112486033, 1112486034, 1112486035, 1112486036]
    })

    expected = pd.DataFrame({
        'userId': [0, 1],
        'Action': [0.0, 0.0],
        'Adventure': [0.4, 0.4]
    })

    expected = expected.set_index('userId')

    user_matrix = create_user_matrix(ratings, movies)
    assert_frame_equal(user_matrix, expected)
