
import os
from pathlib import Path
import joblib
MODELS_PATH = os.getenv("MODELS_PATH")
MODELS_PATH =Path(MODELS_PATH )
def load_model(path=MODELS_PATH / "Random Forest_model.pkl"):
    return joblib.load(path)
