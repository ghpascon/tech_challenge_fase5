import pandas as pd
from fiap.utils.data_processing import remove_unused_columns, remove_null_columns, padronizar_fase


def test_remove_unused_columns():
	df = pd.DataFrame(
		{'nome': ['a', 'b'], 'data_nasc': ['2020', '2021'], 'col1': [1, 2], 'col2': [3, 4]}
	)
	df_clean = remove_unused_columns(df)
	assert 'nome' not in df_clean.columns
	assert 'data_nasc' not in df_clean.columns
	assert 'col1' in df_clean.columns
	assert 'col2' in df_clean.columns


def test_remove_null_columns():
	df = pd.DataFrame(
		{'a': [1, None, None, None], 'b': [1, 2, 3, 4], 'c': [None, None, None, None]}
	)
	df_clean = remove_null_columns(df, 0.5)
	assert 'a' not in df_clean.columns  # >50% nulls
	assert 'c' not in df_clean.columns  # 100% nulls
	assert 'b' in df_clean.columns


def test_padronizar_fase():
	assert padronizar_fase('Fase 1') == '1'
	assert padronizar_fase('alfa') == 'alfa'
	assert padronizar_fase('Fase Alfa') == 'alfa'
	assert padronizar_fase('3') == '3'
	assert padronizar_fase('Fase 7') == '7'
	assert padronizar_fase('fase 8') == '8'
	assert padronizar_fase('outro') == 'outro'
