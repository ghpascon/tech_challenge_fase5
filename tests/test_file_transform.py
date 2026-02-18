import pandas as pd
from fiap.utils.file_transform import excel_to_csv


def test_excel_to_csv(tmp_path):
	# Cria um arquivo Excel temporário
	df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
	df2 = pd.DataFrame({'x': [5, 6], 'y': [7, 8]})
	excel_path = tmp_path / 'test.xlsx'
	with pd.ExcelWriter(excel_path) as writer:
		df1.to_excel(writer, sheet_name='Sheet1', index=False)
		df2.to_excel(writer, sheet_name='Sheet2', index=False)
	output_folder = tmp_path / 'csvs'
	excel_to_csv(excel_path, output_folder)
	# Verifica se os arquivos CSV foram criados
	csv1 = output_folder / 'Sheet1.csv'
	csv2 = output_folder / 'Sheet2.csv'
	assert csv1.exists()
	assert csv2.exists()
	df1_loaded = pd.read_csv(csv1)
	df2_loaded = pd.read_csv(csv2)
	pd.testing.assert_frame_equal(df1, df1_loaded)
	pd.testing.assert_frame_equal(df2, df2_loaded)
