from sklearn.preprocessing import MinMaxScaler
from content_predict import *
from collab_predict import *

def hybride_reco(user_id, titre, num_recommendations=10, alpha=0.7, n=100):

    scaler = MinMaxScaler()
    # Obtenir les recommandations basées sur le contenu
    rec_content = content_based_reco(titre, num_recommendations*n)
    rec_content = rec_content.set_index('title')
    rec_content = rec_content.rename(columns={'score': 'score_content'})
    rec_content['score_content'] = scaler.fit_transform(rec_content[['score_content']])
    print("Recommandations basées sur le contenu pour '{}':\n{}".format(titre, 
rec_content.head(10)))

    # Obtenir les recommandations basées sur le filtrage collaboratif
    rec_collab = collab_reco(user_id, num_recommendations*n)
    rec_collab = rec_collab.set_index('title')
    rec_collab = rec_collab.rename(columns={'note': 'score_collab'})
    rec_collab['score_collab'] = scaler.fit_transform(rec_collab[['score_collab']])
    print("Recommandations collaboratives pour l'utilisateur {}:\n{}".format(user_id, 
rec_collab.head(10)))
    
    # Fusionner les scores
    rec_combined = rec_content.join(rec_collab, how='outer').fillna(0)
    rec_combined['score'] = (alpha * rec_combined['score_content']) +((1 - alpha) * 
rec_combined['score_collab'])

    # Trier et retourner les recommandations
    rec_combined = rec_combined.sort_values('score', ascending=False)
    rec_combined = rec_combined[['score_content', 'score_collab', 'score']].reset_index()
    return rec_combined.head(num_recommendations)


if __name__ == "__main__":
    user_id = 1000
    titre = "Braveheart (1995)"
    recommandations_hybrides = hybride_reco(user_id, titre, num_recommendations=10, alpha=0.7)
    print(recommandations_hybrides)