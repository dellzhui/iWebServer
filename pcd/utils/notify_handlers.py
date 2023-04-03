import json
import logging
import re

from interface.config import iWebServerBaseConfig
from interface.utils.iot_utils import IoTUtils
from pcd.datatype.datatype import DeviceWebRtcConnectionDataType
from pcd.models import DeviceInfo
from pcd.utils.device_utils import DeviceHTTPRequestUtil

Log = logging.getLogger(__name__)


class NotifyHandler:
    def __init__(self):
        self.__handlers = {
            'mqtt': self.__mqtt_handler,
        }
        self._iot_util = IoTUtils(DeviceName=iWebServerBaseConfig.IWEBSERVER_MQTT_USERNAME, DeviceSecret=iWebServerBaseConfig.IWEBSERVER_MQTT_PASSWORD)
        self.__device_util = DeviceHTTPRequestUtil()

    def __get_device_webrtc_connection_info(self, device: DeviceInfo):
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

    def __mqtt_handler_hub_ready(self, container: DeviceInfo, device_webrtc_connection_info_hub: DeviceWebRtcConnectionDataType):
        try:
            device_webrtc_connection_info_container = self.__get_device_webrtc_connection_info(container)
            if (device_webrtc_connection_info_container != None):
                Log.info('container is online')
                # https://www.wolai.com/yang_ids/6Rqoiv5Pa3GA1NZXeXieNu#nRfXCyAHaZGove28yTgVye
                result = self._iot_util.SetHubPublishingAction(
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
                    },
                    timeout_s=10)
                if(result == True):
                    result = self._iot_util.SetHubPublishingAction(
                        publishTopic=f'/sys/{container.productKey}/{container.deviceName}/rrpc/container/request/setHubPublishingAction',
                        paras={
                            'actionName': 'control',
                            'paras': {
                                'control': 'run'
                            }
                        },
                        timeout_s=10)
                    return result
            Log.info('container is offline, we will create it')
            return self.__device_util.create_container(container)
        except Exception as err:
            Log.exception('__mqtt_handler_hub_ready err:[' + str(err) + ']')
        return False

    def __mqtt_handler_container_ready(self, container: DeviceInfo, hub: DeviceInfo):
        try:
            device_webrtc_connection_info_hub = self.__get_device_webrtc_connection_info(hub)
            if (device_webrtc_connection_info_hub != None):
                Log.info('hub is online')
                # https://www.wolai.com/yang_ids/6Rqoiv5Pa3GA1NZXeXieNu#nRfXCyAHaZGove28yTgVye
                result = self._iot_util.SetHubPublishingAction(publishTopic=f'/sys/{container.productKey}/{container.deviceName}/rrpc/container/request/setHubPublishingAction',
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
                                                                     },
                                                               timeout_s=10)
                return result
            Log.info('hub is offline')
            return True
        except Exception as err:
            Log.exception('__mqtt_handler_container_ready err:[' + str(err) + ']')
        return False

    def __mqtt_handler(self, payload: dict):
        logging.info('got data is {}'.format(json.dumps(payload)))
        # TODO：parse other
        try:
            '''
            {
                "topic": "xxx",
                "payload": {
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
            }
            '''
            topic = payload['topic']
            device_webrtc_connection_info = DeviceWebRtcConnectionDataType(info=payload['payload'])

            items = re.findall(re.compile('^/sys/rms/crc/(.*?)/(.*?)/response/publisherReady$', re.S), topic)
            if (len(items) != 1):
                Log.error('parse topic failed')
                return False
            device = DeviceInfo.objects.filter(productKey=items[0][0], deviceName=items[0][1]).last()
            if(device == None):
                Log.error('can not get device')
                return False
            Log.info('handle device {}'.format(device.to_json()))

            bound_device_info = device.get_bound_devices()
            if(bound_device_info == None):
                Log.error('can not get bound device info')
                return False
            if(device.is_hub()):
                return self.__mqtt_handler_hub_ready(container=bound_device_info['container'], device_webrtc_connection_info_hub=device_webrtc_connection_info)
            if (device.is_container()):
                return self.__mqtt_handler_container_ready(container=device, hub=bound_device_info['hub'])
            # TODO: handle stb
        except Exception as err:
            Log.exception('__mqtt_handler err:[' + str(err) + ']')
        return False

    def notify(self, handler_type: str, data: dict):
        if(handler_type == None or handler_type not in self.__handlers):
            return False

        try:
            return self.__handlers[handler_type](data)
        except Exception as err:
            logging.exception('notify err:[' + str(err) + ']')
        return False
