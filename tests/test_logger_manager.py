import logging
import os
import tempfile
from fiap.utils.logger_manager import LoggerManager


def test_logger_manager_creates_log_file():
	with tempfile.TemporaryDirectory() as tmpdir:
		log_path = tmpdir
		logger = LoggerManager(log_path=log_path, base_filename='pytestlog', storage_days=2)
		logging.info('Test log entry')
		logger.close()
		files = [f for f in os.listdir(log_path) if f.endswith('.json')]
		assert any('pytestlog' in f for f in files)
