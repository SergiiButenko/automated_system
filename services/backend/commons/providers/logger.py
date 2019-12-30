import logging

class Logger():
    FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    @staticmethod
    def get_logger(name):
        logging.basicConfig(format=Logger.FORMATTER, datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        return logging.getLogger(name)
