import logging
import mlflow
from pathlib import Path
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np
import pandas as pd
import joblib


def log_extreme_examples(y, X):
	for val in [-2, 2]:
		idx = y[y == val].index
		if not idx.empty:
			# pega a linha correta de X
			linha_X = X.iloc[idx[0]].to_dict()
			logging.info(f'Aluno com defasagem {val}: X={linha_X}, y={y.iloc[idx[0]]}')
		else:
			logging.info(f'Nenhum aluno com defasagem {val} encontrado.')


def treinar_modelos(
	X_train,
	X_test,
	y_train,
	y_test,
	modelos: dict,
	param_grids: dict,
	experiment_name: str,
	model_dir: str,
	random_state: int = 42,
):
	"""
	Treina múltiplos modelos com GridSearchCV + MLflow.

	Retorna:
	    df_resultados (pd.DataFrame)
	    melhor_modelo_geral (sklearn estimator)
	"""

	logging.info('========== INÍCIO DO TREINAMENTO ==========')

	resultados = {}
	cv_mae = {}
	melhores_estimadores = {}
	melhor_r2_geral = -np.inf
	melhor_modelo_geral = None
	melhor_nome_geral = None

	model_path = Path(model_dir)
	model_path.mkdir(parents=True, exist_ok=True)

	mlflow.set_experiment(experiment_name=experiment_name)

	for nome, modelo in modelos.items():
		logging.info(f'Treinando modelo: {nome}')

		try:
			grid = GridSearchCV(
				modelo, param_grids[nome], cv=5, scoring='neg_mean_absolute_error', n_jobs=-1
			)

			grid.fit(X_train, y_train)

			melhor_modelo = grid.best_estimator_
			melhores_estimadores[nome] = melhor_modelo
			cv_mae[nome] = -grid.best_score_

			y_pred = melhor_modelo.predict(X_test)

			mae = mean_absolute_error(y_test, y_pred)
			rmse = np.sqrt(mean_squared_error(y_test, y_pred))
			r2 = r2_score(y_test, y_pred)

			resultados[nome] = {'MAE': mae, 'RMSE': rmse, 'R2': r2, 'CV_MAE': cv_mae[nome]}

			logging.info(
				f'Modelo: {nome} | '
				f'MAE: {mae:.4f} | '
				f'RMSE: {rmse:.4f} | '
				f'R²: {r2:.4f} | '
				f'CV_MAE: {cv_mae[nome]:.4f}'
			)

			with mlflow.start_run(run_name=nome):
				mlflow.log_params(grid.best_params_)
				mlflow.log_metric('MAE', mae)
				mlflow.log_metric('RMSE', rmse)
				mlflow.log_metric('R2', r2)
				mlflow.log_metric('CV_MAE', cv_mae[nome])

				mlflow.sklearn.log_model(
					sk_model=melhor_modelo,
					name='model',
					input_example=X_train[:5],
				)

			# Seleciona melhor modelo pelo R²
			if r2 > melhor_r2_geral:
				melhor_r2_geral = r2
				melhor_modelo_geral = melhor_modelo
				melhor_nome_geral = nome

				joblib.dump(melhor_modelo_geral, model_path / 'best_model.joblib')

				logging.info(
					f'Novo melhor modelo salvo: '
					f'{melhor_nome_geral} com R²={melhor_r2_geral:.4f}'
				)

		except Exception as e:
			logging.error(f'Erro no modelo {nome}: {e}')

	logging.info('========== FIM DO TREINAMENTO ==========')

	df_resultados = pd.DataFrame(resultados).T.sort_values(by='R2', ascending=False)

	logging.info('===== RESULTADOS FINAIS =====')
	logging.info(df_resultados.to_string())
	logging.info(f'Modelo final selecionado: {melhor_nome_geral}')
	logging.info(f"Modelo salvo em: {model_path / 'best_model.joblib'}")

	return df_resultados, melhor_modelo_geral
