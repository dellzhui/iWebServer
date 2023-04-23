import os

from interface.config import iWebServerBaseConfig


class iWebServerConfig(iWebServerBaseConfig):
    # You can customize the desired configuration here

    # permission
    IWEBSERVER_PERMISSION_WORKSTATION_ACCESS = 'workstation_access'
    IWEBSERVER_PERMISSION_ROOM_ACCESS = 'room_access'
    IWEBSERVER_PERMISSION_DEVICE_ACCESS = 'device_access'

    # Error Code
    IWEBSERVER_ERROR_CODE_EMAIL_ALREADY_PRESENCED = -1107
    IWEBSERVER_ERROR_CODE_USERNAME_ALREADY_PRESENCED = -1108
    IWEBSERVER_ERROR_CODE_PASSWORD_NOT_MATCH = -1109
    IWEBSERVER_ERROR_CODE_CHANGING_ADMIN_USER = -1110
    IWEBSERVER_ERROR_CODE_WORKSTATION_ALREADY_PRESENCED = -1111
    IWEBSERVER_ERROR_CODE_WORKSTATION_NOT_PRESENCED = -1112
    IWEBSERVER_ERROR_CODE_ROOM_ALREADY_PRESENCED = -1113
    IWEBSERVER_ERROR_CODE_ROOM_NOT_PRESENCED = -1114
    IWEBSERVER_ERROR_CODE_CREATE_ROOM_FAILED = -1115
    IWEBSERVER_ERROR_CODE_DESTROY_ROOM_FAILED = -1116
    IWEBSERVER_ERROR_CODE_DEVICE_ALREADY_PRESENCED = -1117
    IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED = -1118
    IWEBSERVER_ERROR_CODE_DEVICE_ROOM_FAILED = -1119
    IWEBSERVER_ERROR_CODE_DESTROY_DEVICE_FAILED = -1120

    # janus
    IWEBSERVER_JANUS_BASE_URL = os.environ.get('IWEBSERVER_JANUS_BASE_URL')

    # device
    IWEBSERVER_DEVICE_BASE_URL = os.environ.get('IWEBSERVER_DEVICE_BASE_URL')
    IWEBSERVER_DEVICE_MEETING_CONTRIL_BASE_URL = os.environ.get('IWEBSERVER_DEVICE_MEETING_CONTRIL_BASE_URL')

    # webrtc
    IWEBSERVER_WEBRTC_AUTO_CREATE_CONTAINER_ON_HUB_READY = False if (os.environ.get('IWEBSERVER_WEBRTC_AUTO_CREATE_CONTAINER_ON_HUB_READY', 'True') == 'False') else True

    # auth
    IWEBSERVER_AUTH_BASE_URL = os.environ.get('IWEBSERVER_AUTH_BASE_URL')
    IWEBSERVER_AUTH_LOCAL_HOST = os.environ.get('IWEBSERVER_AUTH_LOCAL_HOST')
