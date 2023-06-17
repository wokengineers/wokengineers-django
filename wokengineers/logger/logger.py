import datetime
import logging.config
from kuantam.logger.filters import CustomLoggerFilter
import pprint
from kuantam.logger.consts import FMT
from kuantam.logger.config import logger_config
import logging


class CustomLogger:

    # Check how can we get the dict (Done).
    # Pass list of variable in filter and check in request if exist then add or else dont add. (Done)
    # Make all variable in constant Capital (Done)
    # Proper error msg. (logger lib is giving proper exceptions as of now)
    # Make single Constant file (Done)
    # Using appname find the respective package and import within library (Done)
    # Move request in middleware package (Done)
    # Versioning in package --> Later
    # Test cases   ---> After review with Yogi

    def __init__(self, filename="", filehandler=False,
                 filehandler_level=logging.DEBUG, streamhandler_level=logging.DEBUG, level=logging.DEBUG,
                 fmt=FMT,
                 filehandler_when="midnight",
                 filehandler_backupcount=0,
                 delimiter=None,
                 filter_dict=None,
                 auto_reload_level = logging.INFO,
                 kafka_logger_level = logging.INFO
                 ):
        self.logger = ""
        self.kafka_logger = "kafka"
        self.auto_reload_logger = "django.utils.autoreload"
        self.filehandler_when = filehandler_when
        self.filehandler_backupcount = filehandler_backupcount
        self.logger_config = logger_config
        self.filename = filename
        self.delimiter = delimiter
        self.fmt = fmt
        self.filter_dict = filter_dict
        self.filehandler_level = filehandler_level
        self.streamhandler_level = streamhandler_level
        self.filehandler = filehandler
        self.level = level
        self.auto_reload_level = auto_reload_level
        self.kafka_logger_level = kafka_logger_level

        self._setformate()
        self._setdelimiter()
        self._set_auto_reload_logger()
        self._set_kafka_logger()
        self._getlogger()
        self._streamhandlerFilter()
        self._addhandlers()

    def __repr__(self):
        return pprint.pformat(self.logger_config)

    def __call__(self):
        return self.logger
        
    def _set_kafka_logger(self):
        self.kafka_logger = logging.getLogger(self.kafka_logger)
        self.kafka_logger.setLevel(self.kafka_logger_level)

    def _set_auto_reload_logger(self):
        self.auto_reload_logger = logging.getLogger(self.auto_reload_logger)
        self.auto_reload_logger.setLevel(self.auto_reload_level)

    def _getlogger(self):
        logging.config.dictConfig(self.logger_config)
        logger = logging.getLogger(self.logger)
        logger.setLevel(self.level)
        self.logger = logger

    def _setdelimiter(self):
        if self.delimiter:
            fmt = self.fmt.replace("^", self.delimiter)
            self.logger_config['formatters']['colored_verbose']["format"] = fmt

    def _setformate(self):
        self.logger_config['formatters']['colored_verbose']["format"] = self.fmt

    def getformate(self):
        return self.logger.handlers[0].formatter

    def _streamhandlerFilter(self):
        stdout_handler = self.logger.handlers[0]
        stdout_handler.setLevel(self.streamhandler_level)
        stdout_handler.addFilter(CustomLoggerFilter(filter_dict=self.filter_dict))
        return stdout_handler

    def _filehandler(self):
        """
        class logging.handlers.TimedRotatingFileHandler(filename, when='h',
                     interval=1, backupCount=0, 
                     encoding=None, 
                     delay=False, utc=False, atTime=None, errors=None)
        """
        file_handler = logging.handlers.TimedRotatingFileHandler(f"{self.filename}.log", when=self.filehandler_when,
                                                                 backupCount=self.filehandler_backupcount,
                                                                 )
        file_handler.setLevel(self.filehandler_level)
        file_handler.setFormatter(self.getformate())
        file_handler.addFilter(CustomLoggerFilter(filter_dict=self.filter_dict))
        return file_handler

    def _addhandlers(self):
        if self.filehandler:
            self.logger.addHandler(self._filehandler())

    @staticmethod
    def printConfig(logger):
        return pprint.pformat(logger.__dict__)
