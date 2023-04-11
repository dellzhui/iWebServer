import os

from interface.config import iWebServerBaseConfig


class MQTTSubscriberServiceConfig(iWebServerBaseConfig):
    # You can customize the desired configuration here

    # pcd
    IWEBSERVER_3D_PCD_BASE_URL = os.environ.get('IWEBSERVER_3D_PCD_BASE_URL')
