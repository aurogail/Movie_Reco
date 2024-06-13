import pandas as pd
from surprise import SVD
from surprise.model_selection import GridSearchCV
from surprise.model_selection import cross_validate
import mlflow
import sys
sys.path.append('src')
from src.models.load_svd_data import load_and_prepare_data


# Define experiment name
experiment_name = "SVD_Grid_Search"
mlflow.set_experiment(experiment_name)

mlflow.autolog()

def grid_search_svd(param_grid, measures=['rmse', 'mae'], cv=3):
    """
    Perform grid search for SVD model using Surprise library
    with given parameter grid and return the best parameters.
    """
    df_surprise,_ = load_and_prepare_data()
    gs = GridSearchCV(SVD, param_grid, measures=measures, cv=cv)
    gs.fit(df_surprise)
    
    print("Best RMSE score:", gs.best_score['rmse'])
    print("Best MAE score:", gs.best_score['mae'])
    print("Best parameters for RMSE:", gs.best_params['rmse'])
    
    return gs.best_params['rmse']

if __name__ == "__main__":
    # Define parameter grid
    param_grid = {'n_factors': [50, 70, 100],
                  'n_epochs': [20, 25, 30],
                  'lr_all': [0.005, 0.01, 0.1],
                  'reg_all': [0.02, 0.05, 0.1]}
    
    with mlflow.start_run():
        # Perform grid search
        best_params_rmse = grid_search_svd(param_grid)
        
        # Log parameters
        mlflow.log_params(best_params_rmse)
        
        # Tuned SVD model with best parameters
        tuned_svd_model = SVD(**best_params_rmse)
        df_surprise, train_set = load_and_prepare_data()
        
        # Evaluate the model
        cv_results = cross_validate(tuned_svd_model, df_surprise, measures=['RMSE', 'MAE'], cv=5, verbose=True)
        
        # Log CV results as artifact
        cv_results_df = pd.DataFrame(cv_results)
        cv_results_df.to_csv("cv_results_grid_search.csv", index=False)
        mlflow.log_artifact("cv_results_grid_serach.csv")