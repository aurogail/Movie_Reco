import logging
import pandas as pd
from datetime import datetime
from sqlalchemy import inspect, text
from src.data.db.database_functions import get_engine

path = "src/data/raw"
current_time = datetime.now()
current_ts = current_time.timestamp()
min_expected_ts = datetime(1995, 1, 1, 0, 0, 0).timestamp()           # we don't expect data prior to 1995

logger = logging.getLogger("airflow.task")

# Use SQL Alchemy engine
engine, inspector = get_engine()

def check_table_details(table_name, expected_schema):

    engine, inspector = get_engine()
    columns = inspector.get_columns(table_name)

    for column in columns:
            column_name = column['name']
            assert column_name in expected_schema, f"Unexpected column {column_name}"
            
            expected_type = expected_schema[column_name]['type']
            actual_type = str(column['type'])
            assert expected_type in actual_type, f"Expected type {expected_type} for column {column_name}, but got {actual_type}"
            
            """expected_nullable = expected_schema[column_name]['nullable']
            actual_nullable = column['nullable']
            assert expected_nullable == actual_nullable, f"Expected nullable={expected_nullable} for column {column_name}, but got nullable={actual_nullable}"

            expected_primary_key = expected_schema[column_name]['primary_key']
            actual_primary_key = column['primary_key']
            assert expected_primary_key == actual_primary_key, f"Expected primary_key={expected_primary_key} for column {column_name}, but got primary_key={actual_primary_key}"
            """



def test_postgre_database_exists():
    """ Checks that the Postgre database exists"""

    # Use SQL Alchemy engine
    engine, inspector = get_engine()
    
    expected_schema = {
        'genome_scores': ['movie_id', 'gtag_id', 'relevance', 'updated_at'],
        'genome_tags': ['gtag_id', 'tag', 'updated_at'],
        'links': ['movie_id', 'imdb_id', 'tmdb_id', 'updated_at'],
        'movies': ['movie_id', 'title', 'genres', 'updated_at'],
        'ratings': ['user_id', 'movie_id', 'rating', 'created_at', 'updated_at'],
        'tags': ['user_id', 'movie_id', 'tag', 'created_at', 'updated_at'],
        'users': ['user_id', 'user_key', 'updated_at'],
        #'predicted_ratings': ['pred_id', 'predicted_rating', 'model', 'feedback'],
        'recommendations': ['reco_id', 'movie_id', 'user_id', 'reco_type', 'reco_datetime', 'user_feedback']
    }

    actual_tables = inspector.get_table_names()
    expected_tables = list(expected_schema.keys())

    # Check if all expected tables are present
    assert(set(expected_tables).issubset(set(actual_tables))), f"Missing tables: {set(expected_tables) - set(actual_tables)}"
    
    # Check if there are any unexpected tables
    assert(set(actual_tables).issubset(set(expected_tables))), f"Unexpected tables: {set(actual_tables) - set(expected_tables)}"


def test_postgre_table_movie():
    """ Checks that movies table is correctly formatted and contained all expected fields """

    expected_schema = {
        'movie_id': {'type': 'INTEGER'},
        'title': {'type': 'VARCHAR(255)'},
        'genres': {'type': 'TEXT'},
        'updated_at': {'type': 'TIMESTAMP'}
    }

    check_table_details("movies", expected_schema)


def test_postgre_table_ratings():
    """ Checks that movies table is correctly formatted and contained all expected fields """

    expected_schema = {
        'user_id': {'type': 'INTEGER'},
        'movie_id': {'type': 'INTEGER'},
        'rating': {'type': 'NUMERIC(2, 1)'},
        'created_at': {'type': 'TIMESTAMP'},
        'updated_at': {'type': 'TIMESTAMP'}
    }

    check_table_details("ratings", expected_schema)

def test_postgre_database_exists():
    """ Vérifie que les tables nécessaires existent dans la base de données PostgreSQL. """
    # Les noms des tables attendues dans la base de données
    expected_tables = ['movies', 'ratings', 'tags', 'genome_scores', 'genome_tags']  # ajustez selon les vrais noms utilisés
    # Récupération des noms des tables existantes dans la base de données
    actual_tables = inspector.get_table_names()
    # Vérification que chaque table attendue existe
    missing_tables = set(expected_tables) - set(actual_tables)
    assert not missing_tables, f"Tables manquantes: {missing_tables}"


def test_table_movies():
    """ Vérifie que la table des films est correctement formatée dans la base de données PostgreSQL. """
    table_name = 'movies'  # Assurez-vous que c'est le nom correct de votre table dans la base de données
    # Récupération des détails des colonnes pour la table spécifiée
    columns = inspector.get_columns(table_name)
    column_details = {col['name']: col['type'].__visit_name__.upper() for col in columns}

    # Définition des colonnes attendues et de leurs types de données
    expected_schema = {
        'movie_id': 'INTEGER',  # Assurez-vous que le nom de la colonne et le type sont corrects
        'title': 'VARCHAR',
        'genres': 'TEXT'
    }

    # Vérification que chaque colonne attendue existe et a le type de données correct
    for col_name, col_type in expected_schema.items():
        assert col_name in column_details, f"Colonne manquante: {col_name}"
        assert column_details[col_name] == col_type, f"Type incorrect pour la colonne {col_name}: trouvé {column_details[col_name]}, attendu {col_type}"

    # Vérification qu'il n'y a pas de colonnes inattendues
    unexpected_columns = set(column_details.keys()) - set(expected_schema.keys())
    assert not unexpected_columns, f"Colonnes inattendues: {unexpected_columns}" 


def test_table_ratings():
    """ Vérifie que la table des évaluations est correctement formatée dans la base de données PostgreSQL. """
    table_name = 'ratings'
    columns = inspector.get_columns(table_name)
    column_details = {col['name']: col['type'].__visit_name__.upper() for col in columns}

    expected_schema = {
        'user_id': 'INTEGER',
        'movie_id': 'INTEGER',
        'rating': 'NUMERIC',
        'created_at': 'TIMESTAMP'  # Changement de 'timestamp' à 'created_at'
    }

    # Vérification que chaque colonne attendue existe et a le type de données correct
    for col_name, col_type in expected_schema.items():
        assert col_name in column_details, f"Colonne manquante: {col_name}"
        assert column_details[col_name] == col_type, f"Type incorrect pour la colonne {col_name}: trouvé {column_details[col_name]}, attendu {col_type}"

    # Vérification des valeurs de la colonne 'rating'
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT rating FROM {table_name}"))
        ratings = [row[0] for row in result]

    # Ajout de vérifications pour s'assurer que les valeurs de 'rating' sont correctes
    valid_ratings = {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0}
    assert all(rating in valid_ratings for rating in ratings), "Les évaluations doivent être parmi les valeurs valides spécifiées"


def test_table_tags():
    """ Vérifie que la table des tags est correctement formatée dans la base de données PostgreSQL. """
    table_name = 'tags'
    columns = inspector.get_columns(table_name)
    column_details = {col['name']: col['type'].__visit_name__.upper() for col in columns}

    expected_schema = {
        'user_id': 'INTEGER',
        'movie_id': 'INTEGER',
        'tag': 'TEXT',
        'created_at': 'TIMESTAMP'  # Assumant que le timestamp est stocké dans 'created_at'
    }

    # Vérification que chaque colonne attendue existe et a le type de données correct
    for col_name, col_type in expected_schema.items():
        assert col_name in column_details, f"Colonne manquante: {col_name}"
        assert column_details[col_name] == col_type, f"Type incorrect pour la colonne {col_name}: trouvé {column_details[col_name]}, attendu {col_type}"


def test_table_genome_scores():
    """ Vérifie que la table des scores du génome est correctement formatée dans la base de données PostgreSQL. """
    table_name = 'genome_scores'
    columns = inspector.get_columns(table_name)
    column_details = {col['name']: col['type'].__visit_name__.upper() for col in columns}

    expected_schema = {
        'movie_id': 'INTEGER',
        'gtag_id': 'INTEGER',  # Assurez-vous que c'est le bon nom de colonne dans votre DB
        'relevance': 'NUMERIC'  # Correction du type de données pour correspondre à la DB
    }

    # Vérification que chaque colonne attendue existe et a le type de données correct
    for col_name, col_type in expected_schema.items():
        assert col_name in column_details, f"Colonne manquante: {col_name}"
        assert column_details[col_name] == col_type, f"Type incorrect pour la colonne {col_name}: trouvé {column_details[col_name]}, attendu {col_type}"



def test_table_genome_tags():
    """ Vérifie que la table des tags du génome est correctement formatée dans la base de données PostgreSQL. """
    table_name = 'genome_tags'
    columns = inspector.get_columns(table_name)
    column_details = {col['name']: col['type'].__visit_name__.upper() for col in columns}

    expected_schema = {
        'gtag_id': 'INTEGER',  # Assurez-vous que c'est le bon nom de colonne dans votre DB
        'tag': 'TEXT'  # Le type de données devrait être TEXT pour correspondre à un champ de chaîne
    }

    # Vérification que chaque colonne attendue existe et a le type de données correct
    for col_name, col_type in expected_schema.items():
        assert col_name in column_details, f"Colonne manquante: {col_name}"
        assert column_details[col_name] == col_type, f"Type incorrect pour la colonne {col_name}: trouvé {column_details[col_name]}, attendu {col_type}"
