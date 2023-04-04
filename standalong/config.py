import os

from interface.config import iWebServerBaseConfig


class MQTTSubscriberServiceConfig(iWebServerBaseConfig):
    # You can customize the desired configuration here

    # log
    IWEBSERVER_LOG_FILENAME = os.environ.get('IWEBSERVER_LOG_FILENAME', 'iwebserver.log')
    IWEBSERVER_LOG_LEVEL = os.environ.get('IWEBSERVER_LOG_LEVEL', 'debug')

    # pcd
    IWEBSERVER_3D_PCD_BASE_URL = os.environ.get('IWEBSERVER_3D_PCD_BASE_URL')
