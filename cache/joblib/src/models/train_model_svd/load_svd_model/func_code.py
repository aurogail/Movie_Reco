# first line: 65
@memory.cache
def load_svd_model(filepath="src/models/svd_model.pkl"):
    with open(filepath, "rb") as filehandler:
        return pickle.load(filehandler)
