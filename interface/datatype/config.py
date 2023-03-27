import os
from pathlib import Path


class iWebServerBaseConfig:
    IWEBSERVER_LOG_DIR = os.environ.get('IWEBSERVER_LOG_DIR', Path(__file__).resolve().parent.parent)

    IWEBSERVER_DB_MYSQL_DBNAME = os.environ.get('IWEBSERVER_DB_MYSQL_DBNAME')
    IWEBSERVER_DB_MYSQL_HOST = os.environ.get('IWEBSERVER_DB_MYSQL_HOST')
    IWEBSERVER_DB_MYSQL_PORT = os.environ.get('IWEBSERVER_DB_MYSQL_PORT')
    IWEBSERVER_DB_MYSQL_USER = os.environ.get('IWEBSERVER_DB_MYSQL_USER')
    IWEBSERVER_DB_MYSQL_PASSWORD = os.environ.get('IWEBSERVER_DB_MYSQL_PASSWORD')
