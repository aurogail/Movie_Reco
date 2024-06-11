import time
from src.models.train_model_svd import *
import os
import sys
sys.path.append('src')
from joblib import Memory

# Initialiser la mémoire cache
cachedir = 'cache'
memory = Memory(cachedir, verbose=0)

if __name__ == "__main__":
    # Mesurer le temps d'exécution du premier appel
    start_time = time.time()
    svd_model = load_svd_model()
    execution_time1 = time.time() - start_time
    print("Execution time 1:", execution_time1)

    # Mesurer le temps d'exécution du deuxième appel
    start_time = time.time()
    svd_model = load_svd_model()
    execution_time2 = time.time() - start_time
    print("Execution time 2:", execution_time2)

