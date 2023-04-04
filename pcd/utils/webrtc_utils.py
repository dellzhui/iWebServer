import logging
from interface.config import iWebServerBaseConfig
from interface.utils.iot_utils import IoTUtils
from interface.utils.tools import CommonTools
from pcd.datatype.datatype import DeviceWebRtcConnectionDataType
from pcd.models import DeviceInfo

Log = logging.getLogger(__name__)


class WebRTCUtil:
    def __init__(self):
        self._iot_util = IoTUtils(DeviceName=iWebServerBaseConfig.IWEBSERVER_MQTT_USERNAME, DeviceSecret=iWebServerBaseConfig.IWEBSERVER_MQTT_PASSWORD)

    def get_device_webrtc_connection_info(self, device: DeviceInfo):
        try:
            result = self._iot_util.InvokeThingService(subscribeTopicList=[f'/sys/{device.productKey}/{device.deviceName}/rrpc/response/webrtc/status/get'],
                                                       publishTopic=f'/sys/{device.productKey}/{device.deviceName}/rrpc/request/webrtc/status/get',
                                                       paras={},
                                                       timeout_s=10)
            if (result != None):
                return DeviceWebRtcConnectionDataType(info=result)
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
                            'control': 'run'
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
