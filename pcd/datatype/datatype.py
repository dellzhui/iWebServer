import json
import logging
from interface.utils.log_utils import loggerr
from interface.datatype.datatype import JsonDatatypeBase, IoTBase
from pcd.models import DeviceInfo

Log = loggerr(__name__).getLogger()


# https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#iZqoAUDZjokXtzfkaGiYqg
class CreateContainerDataType(JsonDatatypeBase):
    def __init__(self, roomIdStr: str, roomJoinPin, macAddress, email):
        self.roomId: str = roomIdStr
        self.joinPin = roomJoinPin
        self.localMac = macAddress
        self.UserEmail = email
        self.jobName = None

        if(email != None and '@' in email):
            self.jobName = email.split('@')[0]

    def __str__(self):
        return self.to_json()


# https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#6BDw9WT2SpktspRtzjZhDk
class DestroyContainerDataType(JsonDatatypeBase):
    def __init__(self, nameSpace, email):
        self.namespace = nameSpace
        self.UserEmail = email
        self.jobName = None

        if(email != None and '@' in email):
            self.jobname = email.split('@')[0]

    def __str__(self):
        return self.to_json()


# https://www.wolai.com/yang_ids/6Rqoiv5Pa3GA1NZXeXieNu#7ARJWCRRd7gQAAgujrQygX
class DeviceWebRtcConnectionDataType(JsonDatatypeBase):
    def __init__(self):
        self.requestId = None
        self.roomId = None
        self.roomJoinPin = None
        self.publisherId = None
        self.privateId = None
        self.localMacAddress = None

    def __str__(self):
        return self.to_json()

    # https://www.wolai.com/yang_ids/6Rqoiv5Pa3GA1NZXeXieNu#7ARJWCRRd7gQAAgujrQygX
    @staticmethod
    def from_request(result: dict):
        try:
            device_webrtc_connection_info = DeviceWebRtcConnectionDataType()
            device_webrtc_connection_info.publisherId = result['publisherId']
            device_webrtc_connection_info.roomId = result['roomId']
            device_webrtc_connection_info.roomJoinPin = result['roomJoinPin']
            device_webrtc_connection_info.privateId = result['privateId']
            device_webrtc_connection_info.localMacAddress = result['localMacAddress']
            return device_webrtc_connection_info
        except Exception as err:
            Log.exception('from_request err:[' + str(err) + ']')
        return None

    @staticmethod
    def from_ready_event(payload):
        try:
            if(isinstance(payload, str)):
                info = json.loads(payload)['RmsResult']['extras']['webrtc']
            elif(isinstance(payload, dict)):
                info = payload['RmsResult']['extras']['webrtc']
            else:
                return None
            device_webrtc_connection_info = DeviceWebRtcConnectionDataType()
            device_webrtc_connection_info.publisherId = info['publisherId']
            device_webrtc_connection_info.roomId = info['roomId']
            device_webrtc_connection_info.roomJoinPin = info['roomJoinPin']
            device_webrtc_connection_info.privateId = info['privateId']
            if('local_mac' in info):
                device_webrtc_connection_info.localMacAddress = info['local_mac']
            return device_webrtc_connection_info
        except Exception as err:
            Log.exception('from_ready_event err:[' + str(err) + ']')
        return None


# https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#5RQCMakV2sMuhQBpbRRkx4
class WebsocketDeviceStatusDataType(IoTBase):
    def __init__(self, info=None, deviceStatus=None):
        self.deviceId: int | None = None
        self.deviceStatus: str | None = deviceStatus
        self.publisherId: int | None = None
        self.privateId: int | None = None
        self.roomId: int | None = None
        self.roomJoinPin: str | None = None
        self.turnServer: str | None = None
        self.turnUserName: str | None = None
        self.turnCredential: str | None = None
        self.rtcbotConnectUrl: str | None = None
        self.noVNCConnectUrl: str | None = None

        IoTBase.__init__(self, info=info)

    def __str__(self):
        return self.to_json()

    '''
        {
            "RequestId": "KlDLdSudRpTV",
            "RmsResult": {
                "code": 0,
                "extras": {
                    "publisherType": "webrtc",
                    "webrtc": {
                        "GroupId": "0000000001_0242ac110001",
                        "UserId": "0000000001",
                        "local_mac": "20:a1:da:23:11:39",
                        "privateId": 1184013529,
                        "publisherId": 8979568362539330,
                        "roomId": 2013,
                        "roomJoinPin": "K8FtAOikRVuSLd2f",
                        "stb_mac": "00:00:00:00:00:00"
                    }
                },
                "msg": "OK"
            }
        }
    '''
    def update_from_ready_event(self, payload: str):
        try:
            info = json.loads(payload)['RmsResult']['extras']['webrtc']
            self.publisherId = info['publisherId']
            self.roomId = info['roomId']
            self.roomJoinPin = info['roomJoinPin']
            self.privateId = info['privateId']
        except Exception as err:
            Log.exception('update_from_request err:[' + str(err) + ']')

    def update_from_device_webrtc_connection_info(self, device_webrtc_connection_info: DeviceWebRtcConnectionDataType):
        try:
            self.publisherId = device_webrtc_connection_info.publisherId
            self.roomId = device_webrtc_connection_info.roomId
            self.roomJoinPin = device_webrtc_connection_info.roomJoinPin
            self.privateId = device_webrtc_connection_info.privateId
        except Exception as err:
            Log.exception('update_from_device_webrtc_connection_info err:[' + str(err) + ']')

    def update_from_device(self, device: DeviceInfo):
        self.deviceId = device.id
        self.turnServer = device.turnServer
        self.turnUserName = device.turnUserName
        self.turnCredential = device.turnCredential
        self.rtcbotConnectUrl = device.rtcbotConnectUrl
        self.noVNCConnectUrl = device.noVNCConnectUrl
