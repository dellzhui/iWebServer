import time

from interface.utils.log_utils import loggerr
from interface.config import iWebServerBaseConfig
from interface.utils.iot_utils import IoTUtils
from interface.utils.tools import CommonTools
from pcd.datatype.datatype import DeviceWebRtcConnectionDataType
from pcd.models import DeviceInfo

Log = loggerr(__name__).getLogger()


class WebRTCUtil:
    def __init__(self):
        self._iot_util = IoTUtils(DeviceName=iWebServerBaseConfig.IWEBSERVER_MQTT_USERNAME, DeviceSecret=iWebServerBaseConfig.IWEBSERVER_MQTT_PASSWORD)

    def get_device_webrtc_connection_info(self, device: DeviceInfo, timeout_s=10):
        try:
            # https://www.wolai.com/yang_ids/6Rqoiv5Pa3GA1NZXeXieNu#bgFTh5JP7DcCAgSLYnLJft
            result = self._iot_util.InvokeThingService(subscribeTopicList=[f'/sys/{device.productKey}/{device.deviceName}/rrpc/response/webrtc/status/get'],
                                                       publishTopic=f'/sys/{device.productKey}/{device.deviceName}/rrpc/request/webrtc/status/get',
                                                       paras={},
                                                       timeout_s=10)
            if (result != None):
                return DeviceWebRtcConnectionDataType.from_request(result=result)
        except Exception as err:
            Log.exception('get_device_webrtc_connection_info err:[' + str(err) + ']')
        return None

    def bind_hub_to_container(self, container: DeviceInfo, device_webrtc_connection_info_hub: DeviceWebRtcConnectionDataType):
        try:
            # https://www.wolai.com/yang_ids/6Rqoiv5Pa3GA1NZXeXieNu#nRfXCyAHaZGove28yTgVye
            result = self._iot_util.InvokeThingServiceWithoutResponse(
                publishTopic=f'/sys/{container.productKey}/{container.deviceName}/rrpc/container/request/setHubPublishingAction',
                paras={
                    'actionName': 'hub',
                    'paras': {
                        'hub': {
                            'action': 'run',
                            'roomId': device_webrtc_connection_info_hub.roomId,
                            'publisherId': device_webrtc_connection_info_hub.publisherId,
                            'privateId': device_webrtc_connection_info_hub.privateId,
                            'roomJoinPin': device_webrtc_connection_info_hub.roomJoinPin
                        }
                    }
                })
            if (result == True):
                result = self._iot_util.InvokeThingServiceWithoutResponse(
                    publishTopic=f'/sys/{container.productKey}/{container.deviceName}/rrpc/container/request/setHubPublishingAction',
                    paras={
                        'actionName': 'control',
                        'paras': {
                            'control': {
                                'action': 'run'
                            }
                        }
                    })
                return result
            Log.error('setHubPublishingAction failed')
            return False
        except Exception as err:
            Log.exception('__bind_hub_to_container err:[' + str(err) + ']')
        return False

    def notify_stb_ready_container(self, stb: DeviceInfo, container: DeviceInfo, device_webrtc_connection_info_container: DeviceWebRtcConnectionDataType):
        try:
            if(stb == None or container == None or device_webrtc_connection_info_container == None):
                return False
            # https://www.wolai.com/yang_ids/3ULPJT5hb1d2yZrm9zfoh6#pSNQd1CB9cnevc9xuvSCrj
            result = self._iot_util.InvokeThingServiceWithoutResponse(
                publishTopic=f'/sys/stb/rms/{stb.productKey}/{stb.deviceName}/response/publisherReady',
                paras={
                    "RequestId": CommonTools.getRamdomString(12),
                    "RmsResult": {
                        "code": 0,
                        "extras": {
                            "publisherType": "webrtc",
                            "webrtc": {
                                "local_mac": container.macAddress,
                                "privateId": f'{device_webrtc_connection_info_container.privateId}',
                                "publisherId": f'{device_webrtc_connection_info_container.publisherId}',
                                "roomId": f'{device_webrtc_connection_info_container.roomId}',
                                'roomJoinPin': f'{device_webrtc_connection_info_container.roomJoinPin}',
                                "stb_mac": stb.macAddress
                            }
                        },
                        "msg": "OK"
                    }
                })
            if (result == True):
                Log.info('notify hub ready container succeed')
                return result
            Log.error('notify hub ready container succeed failed')
            return False
        except Exception as err:
            Log.exception('notify_stb_ready_container err:[' + str(err) + ']')
        return False

    def container_join_to_room(self, container: DeviceInfo, roomId: int, roomJoinPin: str):
        try:
            # https://www.wolai.com/yang_ids/6Rqoiv5Pa3GA1NZXeXieNu#uMTRVtj4iwHSxGHq2MAoe1
            result = self._iot_util.InvokeThingServiceWithoutResponse(
                publishTopic=f'/sys/{container.productKey}/{container.deviceName}/rrpc/request/webrtc/connection/put',
                paras={
                    'requestId': CommonTools.getRamdomString(16),
                    'rrpcParas': {
                        'roomId': roomId,
                        'roomJoinPin': roomJoinPin
                    }
                })
            if (result == True):
                try_count = 10
                while(try_count > 0):
                    device_webrtc_connection_info = self.get_device_webrtc_connection_info(device=container)
                    if(device_webrtc_connection_info != None and device_webrtc_connection_info.roomId == roomId):
                        Log.info('join room {} succeed'.format(roomId))
                        return True
                    try_count -= 1
                    time.sleep(5)
            Log.info('join room {} failed'.format(roomId))
            return False
        except Exception as err:
            Log.exception('container_join_to_room err:[' + str(err) + ']')
        return False