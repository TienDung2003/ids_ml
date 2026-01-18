# core/vectorizer.py
import numpy as np
from .feature_defs import SELECTED_FEATURES

class FeatureVectorizer:
    def vectorize(self, features):
        return np.array(
            [float(features.get(f, 0.0)) for f in SELECTED_FEATURES],
            dtype=np.float32
        ).reshape(1, -1)
