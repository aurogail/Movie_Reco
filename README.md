Movie's Recommendations 
==============================

This project is a starting Pack for MLOps projects based on the subject "movie_recommandation". 

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── api_directory      <- Scripts to execute the API
    │   ├── logs
    │   │   └── api_log.log     <- Logs from api calls
    │   ├── api.py              <- Main api file
    │   ├── generate_token.py   <- Generate and decode token for authentication
    │   ├── preferences.py      <- Generate top 3 genres for a user
    │   └── requests.txt        <- Few curl requests for api's routes
    │
    ├── cache             
    │
    ├── dockerfiles             <- Dockerfiles used in docker-compose
    │   ├── Dockerfile          
    │   ├── Dockerfile_api   
    │   ├── Dockerfile_backup    
    │   └── Dockerfile_mlflow     
    │
    ├── grafana                 <- Ressources used for grafana monitoring
    │   ├── dashboards  
    │   └── datasources     
    │
    ├── MLflow                  <- All mlflow runs and artifacts
    │
    ├── notebooks               <- Jupyter notebooks
    │
    ├── references              <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures             <- Generated graphics and figures to be used in reporting
    │
    ├── src                     <- Source code for use in this project
    │   ├── config              <- Rclone configuration file
    │   ├── dags                <- Contains Airflow DAGs
    │   ├── data                <- Scripts to download or generate data
    │   │   ├── db              <- Scripts to generate postgres database
    │   │   │   ├── initialize_database.py   
    │   │   │   ├── drop_database.pgsql                     
    │   │   │   ├── initialize_database.pgsql 
    │   │   │   └── databas_functions.py   
    │   │   ├── interim                     <- Intermediate data that has been transformed
    │   │   ├── raw                         <- The original, immutable data dump
    │   │   ├── check_structure.py    
    │   │   ├── import_raw_data.py 
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   ├── build_features.py
    │   │   ├── content_features.py
    │   │   └── build_tfidf_matrix.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make predictions
    │   │   │                 
    │   │   ├── temp       <- Temporary csv files for predictions
    │   │   ├── collab_predict.py                   <- Predictions with collaborative filtering model (SVD)
    │   │   ├── content_predict.py                  <- Predictions with content based model
    │   │   ├── grid_seacrh_svd.py                  <- Grid-Search on SVD model
    │   │   ├── hybrid_predict.py                   <- Predictions with hybrid model
    │   │   ├── item_id_mapping.csv
    │   │   ├── load_svd_data.py                    
    │   │   ├── train_model_svd.py                  <- Train and evaluate SVD model
    │   │   ├── train_model_test_surprise.py
    │   │   └── user_id_mapping.csv
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │         └── visualize.py
    │
    ├── tests               <- Unit tests
    │   ├── fixtures              
    │   ├── test_api        <- Unitest for api
    │   ├── test_data       <- Unitest for database
    │   ├── test_features   <- Unitest for features
    │   └── test_models     <- Unitest for models
    │
    ├── .dockerignore 
    ├── .gitignore 
    ├── .env 
    ├── alertmanager.yml
    ├── prometheus_rules.yml
    ├── prometheus.yml
    ├── pytest.ini
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    ├── requirements_backup.txt
    ├── setup.py.txt

------------

## Steps to follow 

Convention : All python scripts must be run from the root specifying the relative file path.
[Update Charles]: To make it work, I had to execute the line commands from src directory

### 1- Create a virtual environment using Virtualenv.

    `python -m venv my_env`

###   Activate it 

    `./my_env/Scripts/activate`

###   Install the packages from requirements.txt  (You can ignore the warning with "setup.py")

    `pip install -r .\requirements.txt`

### 2- Execute import_raw_data.py to import the 4 datasets (say yes when it asks you to create a new folder)

    `python .\data\import_raw_data.py` 

### 3- Execute make_dataset.py initializing `./data/raw` as input file path and `./data/processed` as output file path.

    `python .\data\make_dataset.py`

### 4- Execute build_features.py to preprocess the data (this can take a while)

    `python .\features\build_features.py`

### 5- Execute train_model.py to train the model

    `python .\models\train_model.py`

### 5- Finally, execute predict_model.py file to make the predictions (by default you will be printed predictions for the first 5 users of the dataset). 

    `python .\models\predict_model.py`

### Note that we have 10 recommandations per user

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>


# To launch the API

For now, you need to be in project_root, and execute the following command line:
    `uvicorn src.api_directory.api:app --reload`

Example of possible requests: 
# /login
`curl -X POST "http://localhost:8000/login" -H "Content-Type: application/json" -d '{"user_id": 123}'`

# /welcome
`curl -X GET "http://localhost:8000/welcome" -H "Authorization: Bearer <token>"`

# /recommendations
`curl -X GET "http://localhost:8000/recommendations" -H "Authorization: Bearer <token>"`

# /preferences
`curl -X GET "http://localhost:8000/preferences" -H "Authorization: Bearer <token>"`

# /hybrid
`curl -X POST "http://localhost:8000/hybrid" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"titre": "Braveheart (1995)"}`
