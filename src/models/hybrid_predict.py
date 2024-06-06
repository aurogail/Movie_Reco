from sklearn.preprocessing import MinMaxScaler
import sys
sys.path.append('src')
from src.models.content_predict import *
from src.models.collab_predict import *
from src.models.train_model_svd import load_svd_model

def hybride_reco(user_id, svd_model, titre, num_recommendations=10, alpha=0.8, n=1000):
    """
    Description:
    This function generates hybrid movie recommendations by combining content-based and collaborative filtering scores.

    Args:
    - user_id (int): The ID of the user for whom recommendations are generated.
    - svd_model (surprise.SVD): The trained SVD model for collaborative filtering.
    - titre (str): The title of the movie used for content-based recommendations.
    - num_recommendations (int): The number of recommendations to generate. Defaults to 10.
    - alpha (float): The weight given to content-based recommendations in the final score. Defaults to 0.8.
    - n (int): The scaling factor for the number of initial recommendations considered in each method. Defaults to 1000.

    Returns:
    - DataFrame: A DataFrame containing the top recommended movie titles along with their content-based, collaborative, and final scores.
    """

    # Initialize the normalization method
    scaler = MinMaxScaler()

    # Get content-based recommendations
    print("Calculating content based recommendations")
    rec_content = content_based_reco(titre, num_recommendations*n)
    rec_content = rec_content.set_index('title')
    rec_content = rec_content.rename(columns={'score': 'score_content'})
    rec_content['score_content'] = scaler.fit_transform(rec_content[['score_content']])
    print("Recommandations basées sur le contenu pour '{}':\n{}".format(titre, 
rec_content.head(10)))

    # Get collaborative filtering recommendations
    print("Calculating collaborative based recommendations")
    rec_collab = collab_reco(user_id, svd_model, num_recommendations*n)
    rec_collab = rec_collab.set_index('title')
    rec_collab = rec_collab.rename(columns={'note': 'score_collab'})
    rec_collab['score_collab'] = scaler.fit_transform(rec_collab[['score_collab']])
    print("Recommandations collaboratives pour l'utilisateur {}:\n{}".format(user_id, 
rec_collab.head(10)))
    
    # Merge scores
    rec_combined = rec_content.join(rec_collab, how='outer').fillna(0)
    rec_combined['score'] = (alpha * rec_combined['score_content']) +((1 - alpha) * 
rec_combined['score_collab'])

    # Sort and return recommendations
    rec_combined = rec_combined.sort_values('score', ascending=False)
    rec_combined = rec_combined[['score_content', 'score_collab', 'score']].reset_index()
    return rec_combined.head(num_recommendations)


if __name__ == "__main__":
    svd_model = load_svd_model()
    user_id = 1000
    titre = "Braveheart (1995)"
    #recommandations_hybrides = hybride_reco(user_id, svd_model, titre, num_recommendations=10, alpha=0.7)
    recommandations_hybrides = hybride_reco(user_id, svd_model, titre, num_recommendations=1, alpha=0.7)
    print(recommandations_hybrides)