import pandas as pd
import numpy as np
from fiap.utils.model_train import log_extreme_examples, treinar_modelos
from sklearn.linear_model import LinearRegression


class DummyLogger:
	def __init__(self):
		self.logs = []

	def info(self, msg):
		self.logs.append(msg)

	def error(self, msg):
		self.logs.append(msg)


def test_log_extreme_examples(monkeypatch):
	y = pd.Series([0, 2, -2, 1])
	X = pd.DataFrame({'a': [1, 2, 3, 4]})
	dummy_logger = DummyLogger()
	monkeypatch.setattr('logging.info', dummy_logger.info)
	log_extreme_examples(y, X)
	assert any('defasagem 2' in log for log in dummy_logger.logs)
	assert any('defasagem -2' in log for log in dummy_logger.logs)


def test_treinar_modelos_basic(tmp_path):
	# Pequeno dataset
	X = pd.DataFrame({'a': np.arange(10), 'b': np.arange(10, 20)})
	y = pd.Series(np.arange(10))
	modelos = {'lr': LinearRegression()}
	param_grids = {'lr': {}}
	experiment_name = 'pytest_exp'
	model_dir = tmp_path / 'models'
	df_result, best_model = treinar_modelos(
		X, X, y, y, modelos, param_grids, experiment_name, model_dir
	)
	assert 'lr' in df_result.index
	assert best_model is not None
