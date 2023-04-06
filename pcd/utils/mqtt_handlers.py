import json
import logging
from interface.utils.log_utils import loggerr
import re
from pcd.config import iWebServerConfig
from pcd.datatype.datatype import DeviceWebRtcConnectionDataType
from pcd.models import DeviceInfo
from pcd.utils.device_utils import DeviceHTTPRequestUtil
from pcd.utils.webrtc_utils import WebRTCUtil

Log = loggerr(__name__).getLogger()


class MQTThandlers:
    def __init__(self):
        self.__device_util = DeviceHTTPRequestUtil()
        self.__webrtc_util = WebRTCUtil()

    def __mqtt_handler_hub_ready(self, container: DeviceInfo, device_webrtc_connection_info_hub: DeviceWebRtcConnectionDataType):
        try:
            if(container == None or device_webrtc_connection_info_hub == None):
                return False
            device_webrtc_connection_info_container = self.__webrtc_util.get_device_webrtc_connection_info(container)
            if (device_webrtc_connection_info_container != None):
                Log.info('container is online')
                return self.__webrtc_util.bind_hub_to_container(container, device_webrtc_connection_info_hub)
            if(iWebServerConfig.IWEBSERVER_WEBRTC_AUTO_CREATE_CONTAINER_ON_HUB_READY == True):
                Log.info('container is offline, we will create it')
                return self.__device_util.create_container(container)
        except Exception as err:
            Log.exception('__mqtt_handler_hub_ready err:[' + str(err) + ']')
        return False

    def __mqtt_handler_container_ready(self, container: DeviceInfo, hub: DeviceInfo, stb: DeviceInfo, device_webrtc_connection_info_container: DeviceWebRtcConnectionDataType):
        try:
            self.__webrtc_util.notify_stb_ready_container(stb=stb, container=container, device_webrtc_connection_info_container=device_webrtc_connection_info_container)
            device_webrtc_connection_info_hub = self.__webrtc_util.get_device_webrtc_connection_info(hub)
            if (device_webrtc_connection_info_hub != None):
                Log.info('hub is online')
                return self.__webrtc_util.bind_hub_to_container(container, device_webrtc_connection_info_hub)
            Log.info('hub is offline')
            return True
        except Exception as err:
            Log.exception('__mqtt_handler_container_ready err:[' + str(err) + ']')
        return False

    def notify(self, payload: dict):
        Log.info('got data is {}'.format(json.dumps(payload)))
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

            items = re.findall(re.compile('^/sys/rms/crc/(.*?)/(.*?)/response/publisherReady$', re.S), topic)
            # TODO：parse other
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
                device_webrtc_connection_info_hub = DeviceWebRtcConnectionDataType.from_ready_event(payload['payload'])
                return self.__mqtt_handler_hub_ready(container=bound_device_info['container'], device_webrtc_connection_info_hub=device_webrtc_connection_info_hub)
            if (device.is_container()):
                device_webrtc_connection_info_container = DeviceWebRtcConnectionDataType.from_ready_event(payload['payload'])
                return self.__mqtt_handler_container_ready(container=device, hub=bound_device_info['hub'], stb=bound_device_info['stb'], device_webrtc_connection_info_container=device_webrtc_connection_info_container)
            # TODO: handle stb
        except Exception as err:
            Log.exception('__mqtt_handler err:[' + str(err) + ']')
        return False
