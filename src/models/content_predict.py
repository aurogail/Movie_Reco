from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import pandas as pd
import sys
sys.path.append('src')
sys.path.append("../") 
import os
from features.build_tfidf_matrix import calculer_matrice_tfidf

# Load the DataFrame containing movie tags
df_content_tags = pd.read_csv("../data/interim/movies_tags.csv")
# df_content_tags = pd.read_csv("../../tests/fixtures/movies_tags_test.csv")
'''
def is_running_under_pytest():
    return 'pytest' in sys.modules

if is_running_under_pytest():
    df_content_tags = pd.read_csv("tests/fixtures/movies_tags_test.csv")   # pour les tests
else:
    df_content_tags = pd.read_csv("src/data/interim/movies_tags.csv")
'''

def content_based_reco(titre, num_recommendations=10):
    """
    Description:
    This function generates content-based movie recommendations based on the provided movie title and similarity matrix.

    Args:
    - titre (str): The title of the movie for which recommendations are generated.
    - mat_sim (array-like): The similarity matrix used for recommendation.
    - num_recommendations (int): The number of recommendations to generate. Defaults to 3.

    Returns:
    - dict: A dictionary containing movie titles as keys and their similarity scores as values.
    """
    # Calculate TF-IDF matrix calculate_matrix_tfidf is in src/features/build_tfidf_matrix.py
    matrice_tfidf = calculer_matrice_tfidf(df_content_tags)

    # Create an index series
    indices = pd.Series(range(0, len(df_content_tags)), index=df_content_tags.title)


    # Get the index of the provided movie title
    idx = indices[titre]

    # Calculate similarity matrices
    sim_cos = cosine_similarity(matrice_tfidf, matrice_tfidf)   

    # Calculate similarity scores between the provided movie and all other movies and sort in descsending order
    scores_similarite = list(enumerate(sim_cos[idx]))
    scores_similarite = sorted(scores_similarite, key=lambda x: x[1], reverse=True)

    # Select the top similar movies excluding the provided movie itself
    top_similar = scores_similarite[1:num_recommendations+1]

    # Create a dictionary containing recommended movie titles and their similarity scores
    recommandations = [(indices.index[idx], score) for idx, score in top_similar]
    recommandations = pd.DataFrame(recommandations)
    recommandations = recommandations.rename(columns={0: 'title', 1: 'score'})

    return recommandations

if __name__ == "__main__":
    recommandations = content_based_reco('Toy Story (1995)')
    print(recommandations)

