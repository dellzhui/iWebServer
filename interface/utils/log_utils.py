import logging.handlers
from interface.config import iWebServerBaseConfig


class loggerr(object):
    def __init__(self, name, log_level_name='debug'):
        self.__logger = logging.getLogger(name)
        self.__log_level = self.__get_level(log_level_name)
        self.__logger.setLevel(self.__log_level)
        self.fmt = logging.Formatter('[%(levelname)s][%(asctime)s][%(threadName)s:%(thread)d][%(name)s][%(funcName)s:%(lineno)d]%(message)s')

    def __get_level(self, log_level_name):
        if(log_level_name == 'debug'):
            return logging.DEBUG
        if (log_level_name == 'info'):
            return logging.INFO
        if (log_level_name == 'warning'):
            return logging.WARNING
        if (log_level_name == 'error'):
            return logging.ERROR
        return logging.DEBUG


    def __get_file_handler(self):
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename='{}/{}'.format(iWebServerBaseConfig.IWEBSERVER_LOG_DIR, iWebServerBaseConfig.IWEBSERVER_LOG_FILENAME),
            when='W0',
            interval=1,
            backupCount=12,
            encoding='utf-8'
        )
        file_handler.setFormatter(self.fmt)
        file_handler.setLevel(self.__log_level)
        return file_handler

    def __get_stream_hanler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.fmt)
        stream_handler.setLevel(self.__log_level)
        return stream_handler

    def getLogger(self):
        self.__logger.addHandler(self.__get_file_handler())
        self.__logger.addHandler(self.__get_stream_hanler())
        return self.__logger
