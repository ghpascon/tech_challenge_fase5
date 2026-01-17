import pandas as pd
from pathlib import Path
from typing import Union
import logging


def excel_to_csv(excel_path: Union[str, Path], output_folder: Union[str, Path]) -> None:
	"""
	Converte cada planilha de um arquivo Excel em arquivos CSV separados.

	Esta função lê um arquivo Excel e exporta cada aba/planilha como um arquivo CSV
	individual na pasta de saída especificada. Os arquivos CSV são nomeados usando
	o nome original da planilha.

	Args:
	    excel_path (Union[str, Path]): Caminho completo para o arquivo Excel (.xlsx, .xls).
	    output_folder (Union[str, Path]): Caminho da pasta onde os arquivos CSV serão salvos.
	        A pasta será criada automaticamente se não existir.

	Returns:
	    None

	Raises:
	    FileNotFoundError: Se o arquivo Excel não for encontrado.
	    ValueError: Se o arquivo não for um formato Excel válido.
	    PermissionError: Se não houver permissão para criar a pasta de saída ou escrever os arquivos.

	Example:
	    >>> excel_to_csv('dados.xlsx', 'output')
	    >>> # Isso criará arquivos como: output/Planilha1.csv, output/Planilha2.csv, etc.
	"""
	# Converte os caminhos para objetos Path
	excel_path = Path(excel_path)
	output_folder = Path(output_folder)

	# Verifica se o arquivo Excel existe
	if not excel_path.exists():
		raise FileNotFoundError(f'Arquivo Excel não encontrado: {excel_path}')

	# Verifica se é um arquivo Excel válido
	if excel_path.suffix.lower() not in ['.xlsx', '.xls', '.xlsm']:
		raise ValueError(
			f'Formato de arquivo inválido: {excel_path.suffix}. Use .xlsx, .xls ou .xlsm'
		)

	# Cria a pasta de saída se não existir
	output_folder.mkdir(parents=True, exist_ok=True)

	# Lê todas as planilhas do arquivo Excel
	excel_file = pd.ExcelFile(excel_path)

	logging.info(f'Processando arquivo: {excel_path.name}')
	logging.info(f'Total de planilhas encontradas: {len(excel_file.sheet_names)}\n')

	# Itera sobre cada planilha e salva como CSV
	for sheet_name in excel_file.sheet_names:
		# Lê a planilha
		df = pd.read_excel(excel_file, sheet_name=sheet_name)

		# Cria nome do arquivo CSV (remove caracteres inválidos)
		safe_sheet_name = ''.join(
			c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')
		).strip()
		csv_filename = f'{safe_sheet_name}.csv'
		csv_path = output_folder / csv_filename

		# Salva como CSV
		df.to_csv(csv_path, index=False, encoding='utf-8-sig')

		logging.info(f"✓ Planilha '{sheet_name}' convertida para: {csv_filename}")
		logging.info(f'  Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas')

	logging.info(
		f'\n✓ Conversão concluída! {len(excel_file.sheet_names)} arquivo(s) CSV criado(s) em: {output_folder}'
	)
