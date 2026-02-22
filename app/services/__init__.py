from .ml_service import MlManager
from app.core import ML_PATH, DOCS_PATH

ml_manager = MlManager(ML_PATH, DOCS_PATH, 'best_model.joblib')
