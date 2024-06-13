Project Name
==============================

This project is a starting Pack for MLOps projects based on the subject "movie_recommandation". It's not perfect so feel free to make some modifications on it.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── api_directory      <- Scripts to execute the API
    │   ├── api_requirements.txt
    │   ├── api.py
    │   ├── generate_token.py 
    │   ├── preferences.py
    │   └── requests.txt
    │
    ├── cache    
    │
    ├── logs               <- Logs from training and predicting
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   ├── dags           <- Contains Airflow DAGs
    │   ├── data           <- Scripts to download or generate data
    │   │   ├── db
    │   │   │   └── initialize_database.py    
    │   │   ├── interim                     <- Intermediate data that has been transformed.
    │   │   ├── processed                   <- The final, canonical data sets for modeling.
    │   │   ├── raw                         <- The original, immutable data dump.
    │   │   ├── check_structure.py    
    │   │   ├── import_raw_data.py 
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   ├── content_features.py
    │   │   └── build_tfidf_matrix.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   ├── visualization  <- Scripts to create exploratory and results oriented visualizations
    │   │   └── visualize.py
    │   └── config         <- Describe the parameters used in train_model.py and predict_model.py
    │
    ├── tests              <- Unit tests
    

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
