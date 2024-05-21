from sqlalchemy import create_engine, text, inspect
import pandas as pd
import os
from datetime import datetime

username = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DB')

#host = '127.0.0.1'
#host = 'localhost'
host = 'postgres-db' 
port = '5432'  # default PostgreSQL port is 5432

# Create the database engine
try:
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}', echo=True)
    inspector = inspect(engine)
    print('Connection to database succeeded')
except Exception as e:
    print(e)
    print(username, password, database)
    print('Connection to database failed')


def get_engine():
    return engine, inspector


def sql(query):
    with engine.connect() as conn:
        conn.execute(text(query))


def execute_pgsql_query(filename):
    """ Executes a SQL Query in the SQL Alchemy Engine """
    with open(filename, 'r') as file:
        query = file.read()
    sql(query)


def init_csv_to_sql(table_name, csv_path, mapping):
    """ Feed a table in the postgresDB from a CSV file"""
    df = pd.read_csv(csv_path)
    df = df.rename(columns = mapping)
    now = datetime.now()
    df['updated_at'] = now

    try:
        print(f'Injecting initial data into {table_name}')
        df.to_sql(table_name, engine, if_exists='append', index=False)
    except Exception as e:
        print(e)
        print(f'Injection of table {table_name} failed')

def create_initial_users():
    """ Feed the table 'users' in the postgresDB """
    users = pd.read_csv('../raw/ratings.csv')
    users = users.drop(columns = {'movieId', 'rating', 'timestamp'})
    users = users.drop_duplicates()
    now = datetime.now()
    users['user_key'] = users['userId']        # To be encoded later ?
    users['updated_at'] = now

    try:
        print(f'Injecting initial data into users')
        users.to_sql("users", engine, if_exists='append', index=False)
    except Exception as e:
        print(e)
        print(f'Injection of table users failed')