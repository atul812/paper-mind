import os
import pickle

def save_cache(data,path):
    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(path,"wb") as f:
        pickle.dump(
            data,
            f
        )

def load_cache(path):
    if not os.path.exists(path):
        return None

    with open(path,"rb") as f:
        return pickle.load(f)