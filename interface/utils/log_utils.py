import logging.handlers
from interface.config import iWebServerBaseConfig


class loggerr(object):
    def __init__(self, name, log_level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.fmt = logging.Formatter('[%(levelname)s][%(asctime)s][%(threadName)s:%(thread)d][%(name)s][%(funcName)s:%(lineno)d]%(message)s')
        self.__log_level = log_level

    def __get_file_handler(self):
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename='{}/webrtc_h5.log'.format(iWebServerBaseConfig.IWEBSERVER_LOG_DIR),
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
        self.logger.addHandler(self.__get_file_handler())
        self.logger.addHandler(self.__get_stream_hanler())
        return self.logger
