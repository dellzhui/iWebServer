import os


class iWebServerConfig:
    IWEBSERVER_LOG_DIR = os.environ.get('IWEBSERVER_LOG_DIR', '.')
