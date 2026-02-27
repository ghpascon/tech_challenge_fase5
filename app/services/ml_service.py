from pathlib import Path
import joblib
import logging
import json
import pandas as pd


class MlManager:
	def __init__(self, ml_path: str, docs_path: str, ml_model: str):
		# load model
		try:
			self.model = self._load_model(ml_path, ml_model)
			logging.info(f'Model loaded successfully: {ml_model}')
		except Exception as e:
			logging.error(f'Error loading model: {e}')
			self.model = None

		# load scaler
		try:
			self.scaler = self._load_model(ml_path, 'scaler.joblib')
			logging.info('Scaler loaded successfully: scaler.joblib')
		except Exception as e:
			logging.error(f'Error loading scaler: {e}')
			self.scaler = None

		# load feature names
		try:
			self.feature_names = self._load_model(ml_path, 'feature_names.joblib')
			logging.info('Feature names loaded successfully: feature_names.joblib')
		except Exception as e:
			logging.error(f'Error loading feature names: {e}')
			self.feature_names = None

		# load intitutions data (json)
		try:
			with open(Path(docs_path) / 'map_instituicao_ensino.json', 'r', encoding='utf-8') as f:
				self.institutions_data = json.load(f)
			logging.info('Institutions data loaded successfully: map_instituicao_ensino.json')
		except Exception as e:
			logging.error(f'Error loading institutions data: {e}')
			self.institutions_data = None

	def _load_model(self, ml_path: str, ml_model: str):
		model_path = Path(ml_path) / ml_model
		if not model_path.exists():
			raise FileNotFoundError(f'Model file not found: {model_path}')

		return joblib.load(model_path)

	def predict(self, data) -> float:
		"""Predict the target value from a PredictSchema instance.

		Steps:
		1. Build a flat dict with numeric features.
		2. One-hot encode `genero` → genero_f / genero_m.
		3. One-hot encode `instituicao_tipo` → instituição_tipo_1 … instituição_tipo_7.
		4. Assemble a DataFrame ordered by `self.feature_names`.
		5. Scale with the loaded MinMaxScaler.
		6. Return the Regressor prediction.
		"""
		if self.model is None:
			raise RuntimeError('Model is not loaded')
		if self.scaler is None:
			raise RuntimeError('Scaler is not loaded')
		if self.feature_names is None:
			raise RuntimeError('Feature names are not loaded')

		row: dict = {
			'fase': data.fase,
			'idade': data.idade,
			'iaa': data.iaa,
			'ieg': data.ieg,
			'ips': data.ips,
			'ipp': data.ipp,
			'ida': data.ida,
			'mat': data.mat,
			'por': data.por,
			'ipv': data.ipv,
			#'ian': data.ian,
		}

		# one-hot: genero
		for g in ('f', 'm'):
			row[f'genero_{g}'] = 1.0 if data.genero == g else 0.0

		# one-hot: instituição_tipo  (note: accented column names match feature_names)
		for i in range(1, 8):
			row[f'instituição_tipo_{i}'] = 1.0 if data.instituicao_tipo == i else 0.0

		# build DataFrame in the exact feature order the model was trained on
		df = pd.DataFrame([row])[self.feature_names]

		# scale and predict
		df_scaled = self.scaler.transform(df)
		prediction = self.model.predict(df_scaled)

		return float(prediction[0])
