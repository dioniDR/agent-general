# core.py

import logging

class Core:
    def __init__(self, config):
        self.config = config
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if self.config.get('debug') else logging.INFO)
        return logger

    def run(self):
        self.logger.info("Core module is running.")
        # Add core functionality here

    def shutdown(self):
        self.logger.info("Core module is shutting down.")
        # Add cleanup code here