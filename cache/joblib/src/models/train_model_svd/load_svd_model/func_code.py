# first line: 147
@memory.cache
def load_svd_model(filepath="./src/models/svd_model.pkl"):
    """
    Description:
    This function loads a previously trained SVD model from a file and returns it.

    Args:
    None

    Returns:
    - SVD: The loaded SVD model.
    """
    
    with open(filepath, "rb") as filehandler:
        return pickle.load(filehandler)
