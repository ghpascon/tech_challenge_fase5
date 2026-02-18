import logging
import pandas as pd
import re


def remove_unused_columns(df: pd.DataFrame):
	# Colunas que serão removidas (ajuste conforme necessário)
	unused_columns = [
		col
		for col in df.columns
		if col.startswith('nome')
		or col.startswith('data')
		or col.startswith('ano')
		or col.startswith('ra')
		or col.startswith('avaliador')
		or col.startswith('nº')
		or col.startswith('turma')
	]

	if unused_columns:
		logging.info(f'Removendo {len(unused_columns)} colunas desnecessárias: {unused_columns}')
		df = df.drop(columns=unused_columns)
		logging.info(f'DataFrame após limpeza: {df.shape[0]} linhas, {df.shape[1]} colunas')
	else:
		logging.info('Nenhuma coluna desnecessária encontrada')
	return df


def remove_null_columns(df: pd.DataFrame, threshold_percentage: float):
	# Remover colunas que tenham mais de 30% de valores nulos
	threshold = len(df) * threshold_percentage
	cols_to_drop = df.columns[df.isnull().sum() > threshold]
	if len(cols_to_drop) > 0:
		logging.info(
			f'Removendo {len(cols_to_drop)} colunas com mais de 30% de valores nulos: {list(cols_to_drop)}'
		)
		df = df.drop(columns=cols_to_drop)
		logging.info(
			f'DataFrame após remoção de colunas nulas: {df.shape[0]} linhas, {df.shape[1]} colunas'
		)
	return df


# Padronização da coluna "fase"
def padronizar_fase(valor):
	v = str(valor).strip().lower()
	v = v.replace('fase ', '')  # Remove o prefixo "fase " se existir
	if v.startswith('alfa'):
		return 'alfa'
	# Extrai o primeiro número encontrado (1-8) para as fases

	match = re.search(r'[1-8]', v)
	if match:
		return f'{match.group(0)}'
	return v
