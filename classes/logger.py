import logging
import traceback
import sys

class Logger():
    def __init__(self, name : str, path : str = None):
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        if not path.endswith("/"):
            path += "/"
        
        path = path + name + ".log"

        # Create file handler
        self.fh = logging.FileHandler(path)
        self.fh.setLevel(logging.DEBUG)
        # Create console handler
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        # Set Formatter
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)
        # Add Handler
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

    async def debug(self, text):
        self.logger.debug(text)

    async def info(self, text):
        self.logger.info(text)

    async def error(self, text):
        self.logger.error(text)

    async def critical(self, text):
        self.logger.critical(text)