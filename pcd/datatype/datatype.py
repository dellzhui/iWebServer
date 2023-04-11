import json
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

# https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#6BDw9WT2SpktspRtzjZhDk
class DeViceMeDataType(JsonDatatypeBase):
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
class WebsocketDeviceStatusDataType(JsonDatatypeBase):
    def __init__(self, device: DeviceInfo, deviceStatus=None):
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
        self.meetingId: str | None = None
        self.meetingUrl: str | None = None
        self.meetingJoined: bool = False

        self.update_from_device(device)

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
        self.meetingId = device.meetingId
        self.meetingUrl = device.meetingUrl
        self.meetingJoined = device.meetingJoined


# https://www.wolai.com/yang_ids/bg4kyCjfdMqSza4qc7tTvF#aNAcSKDn8zTAszr4VyJQ2b
class WebsocketMeetingInfoDataType(JsonDatatypeBase):
    def __init__(self, device: DeviceInfo):
        self.deviceId: int = device.id
        self.meetingId: str | None = None
        self.meetingUrl: str | None = None
        self.meetingJoined: bool = True if(device.meetingJoined) else False
        self.meetingName: str | None = None
        self.meetingBeginTime: str | None = None
        self.meetingEndTime: str | None = None
        self.meetingRoomId: int | None = None
        self.meetingRoomJoinPin: str | None = None
        self.meetingStatus: str | None = None

    # https://www.wolai.com/yang_ids/bg4kyCjfdMqSza4qc7tTvF#ksbxPC85Qw5j93fyBLtHMp
    def update_from_request_result(self, result: dict):
        try:
            self.meetingId = result['meeting_id']
            self.meetingUrl = result['meeting_control_index_url']
            self.meetingName = result['meeting_name']
            self.meetingBeginTime = result['meeting_start_time']
            self.meetingEndTime = result['meeting_end_time']
            self.meetingRoomId = int(result['roomId'])
            self.meetingRoomJoinPin = result['roomJoinPin']
            if(result['current_meeting_status'] == 'over'):
                self.meetingStatus = 'Ended'
            elif(result['current_meeting_status'] == 'not started'):
                self.meetingStatus = 'NotStarted'
            elif(result['current_meeting_status'] == 'running'):
                self.meetingStatus = 'Running'
            return True
        except Exception as err:
            Log.exception('update_from_request err:[' + str(err) + ']')
        return False
