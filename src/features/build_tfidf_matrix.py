import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def calculer_matrice_tfidf(df='../data/interim/movies_tags.csv'):
    """
    This function takes a DataFrame containing movie tags and returns the corresponding TF-IDF matrix.
    
    Args:
    - df : pandas DataFrame containing movie tags (tags = genres+tags)
    
    Returns:
    - tfidf_matrix : TF-IDF matrix of movie tags
    """

    df.dropna(subset=['all_tags'], inplace=True)
    
    # Initialize the TF-IDF vectorizer
    tfidf = TfidfVectorizer()

    # Calculate the TF-IDF matrix
    matrice_tfidf = tfidf.fit_transform(df['all_tags'])

    return matrice_tfidf

