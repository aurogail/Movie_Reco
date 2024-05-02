#import sys
import pandas as pd
#sys.path.append('src')

from models.train_model import train_model

def test_create_model():
    """ Checks that the model can be created with a basic movie matrix"""

    movie_matrix = pd.read_csv('tests/fixtures/movie_matrix_test.csv')
    model = train_model(movie_matrix)
