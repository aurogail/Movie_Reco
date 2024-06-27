#!/bin/bash
# Arrêter le script si une commande échoue
set -e
mkdir ./MLflow
mkdir ./cache

# Charger les variables d'environnement du fichier .env
source .env

# Définir la variable d'environnement
export MLFLOW_BACKEND_URI="./MLflow"
echo "MLFLOW_BACKEND_URI définie à $MLFLOW_BACKEND_URI"

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Exécution des scripts pour les données
echo "Importation des données brutes..."
python3 src/data/import_raw_data.py
echo "Création du dataset..."
input_filepath="src/data/raw/"
output_filepath="src/data/processed"
python3 src/data/make_dataset.py "$input_filepath" "$output_filepath"

# Exécution des scripts pour les features
echo "Construction des features..."
python3 src/features/build_features.py

# Démarrage des services Docker
echo "Démarrage des services Docker..."
docker-compose up --build -d

# Copie le backup database dans le volume pg_project_data
docker container exec -it rclone_docker rclone copyto recofilm:recofilm_db/recofilm_gdrive_300K.sql db/recofilm_gdrive.sql -vv

# Restaure la DB
docker container exec -it postgres_db pg_restore -U admin -d recofilm_db -F c var/lib/postgresql/data/db/recofilm_gdrive.sql

# Unpause du DAG
echo "Activation du DAG train_model dans Airflow..."
docker exec -it airflow_webserver airflow dags unpause train_model

# Triggering du DAG
echo "Déclenchement du DAG train_model dans Airflow..."
docker exec -it airflow_webserver airflow dags trigger train_model

# Creation de movies_tags.csv (peut prendre quelques minutes)
echo "Extraction des features de contenu..."
docker exec -it airflow_webserver python ./src/features/content_features.py
echo "Construction de la matrice TF-IDF..."
docker exec -it airflow_webserver python ./src/features/build_tfidf_matrix.py

# Relancer le conteneur api_docker
echo "Relance du conteneur api_docker..."
docker-compose up -d api
echo "Prêt à être utilisé."
