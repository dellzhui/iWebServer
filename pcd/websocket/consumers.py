import json
from interface.utils.log_utils import loggerr
import re
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from pcd.config import iWebServerConfig
from pcd.datatype.datatype import WebsocketDeviceStatusDataType
from pcd.models import DeviceInfo
from pcd.utils.device_utils import DeviceHTTPRequestUtil
from pcd.utils.webrtc_utils import WebRTCUtil
from websocket.consumers import iWebServerConsumer

Log = loggerr(__name__).getLogger()


class PCDConsumer(iWebServerConsumer):
    def __init__(self):
        super().__init__()
        self.__handlers = {
            'container_status': self.__container_status,
            'container_create': self.__container_create,
            'container_destroy': self.__container_destroy,
            'container_reconnect_to_hub': self.__container_reconnect_to_hub,
        }
        self.__device_util = DeviceHTTPRequestUtil()
        self.__webrtc_util = WebRTCUtil()

    def __container_status(self, requestId, paras):
        try:
            device = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if(device == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not device.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)

            device_webrtc_connection_info_container = self.__webrtc_util.get_device_webrtc_connection_info(device)
            if(device_webrtc_connection_info_container != None):
                data = WebsocketDeviceStatusDataType(deviceStatus='ONLINE')
                data.update_from_device_webrtc_connection_info(device_webrtc_connection_info_container)
                data.update_from_device(device)
                return IoTSuccessResponse().GenJson(data=data.to_dict(), requestId=requestId)
            return IoTSuccessResponse().GenJson(data=WebsocketDeviceStatusDataType(deviceStatus='OFFLINE').to_dict(), requestId=requestId)
        except Exception as err:
            Log.exception('__container_status err:[' + str(err) + ']')
        return IoTErrorResponse.GenJson(requestId=requestId)

    def __container_create(self, requestId, paras):
        try:
            device = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if(device == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not device.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)
            if(self.__webrtc_util.get_device_webrtc_connection_info(device, timeout_s=5) != None):
                return IoTErrorResponse.GenJson(error_msg='container already started', requestId=requestId)
            result = self.__device_util.create_container(device)
            if(result == True):
                return IoTSuccessResponse().GenJson(requestId=requestId)
            return IoTErrorResponse.GenJson(error_msg='create container failed', requestId=requestId)
        except Exception as err:
            Log.exception('__container_create err:[' + str(err) + ']')
        return IoTErrorResponse.GenJson(requestId=requestId)

    def __container_destroy(self, requestId, paras):
        try:
            device = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if (device == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not device.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)
            if (self.__webrtc_util.get_device_webrtc_connection_info(device, timeout_s=5) == None):
                return IoTErrorResponse.GenJson(error_msg='container already stopped', requestId=requestId)
            result = self.__device_util.destroy_container(device)
            if (result == True):
                return IoTSuccessResponse().GenJson(requestId=requestId)
            return IoTErrorResponse.GenJson(error_msg='destroy container failed', requestId=requestId)
        except Exception as err:
            Log.exception('__container_destroy err:[' + str(err) + ']')
        return IoTErrorResponse.GenJson(requestId=requestId)

    def __container_reconnect_to_hub(self, requestId, paras):
        try:
            container = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if(container == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not container.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)

            bound_device_info = container.get_bound_devices()
            if (bound_device_info == None or bound_device_info['hub'] == None):
                Log.error('can not get bound hub info')
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='can not get bound hub info', requestId=requestId)

            hub = bound_device_info['hub']
            device_webrtc_connection_info_container = self.__webrtc_util.get_device_webrtc_connection_info(container)
            if(device_webrtc_connection_info_container == None):
                Log.error('container not online')
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='container not online', requestId=requestId)

            device_webrtc_connection_info_hub = self.__webrtc_util.get_device_webrtc_connection_info(hub)
            if (device_webrtc_connection_info_hub == None):
                Log.error('hub not online')
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='hub not online', requestId=requestId)
            if(self.__webrtc_util.bind_hub_to_container(container, device_webrtc_connection_info_hub) == False):
                return IoTErrorResponse.GenJson(error_msg='bind failed', requestId=requestId)
            return IoTSuccessResponse().GenJson(data='bind succeed', requestId=requestId)
        except Exception as err:
            Log.exception('__container_status err:[' + str(err) + ']')
        return IoTErrorResponse.GenJson(requestId=requestId)

    @property
    def _sub_topic_list(self):
        if (self._user == None):
            Log.error('invalid user')
            return None
        sub_list = []
        for device in DeviceInfo.objects.filter(owner_id=self._user.id):
            if(device.productKey != None and device.deviceName != None):
                sub_list.append('/sys/rms/crc/{}/{}/response/publisherReady'.format(device.productKey, device.deviceName))
        Log.info('got sub list is {}'.format(sub_list))
        return sub_list

    def _on_mqtt_msg_cb(self, topic, msg):
        try:
            items = re.findall(re.compile('^/sys/rms/crc/(.*?)/(.*?)/response/publisherReady$', re.S), topic)
            if (len(items) == 1):
                device = DeviceInfo.objects.filter(productKey=items[0][0], deviceName=items[0][1], owner_id=self._user.id).last()
                if(device != None):
                    data = WebsocketDeviceStatusDataType(deviceStatus='ONLINE')
                    data.update_from_ready_event(msg)
                    data.update_from_device(device)
                    return self.send(text_data=data.to_json())
        except Exception as err:
            Log.exception('_on_mqtt_msg_cb err:[' + str(err) + ']')

    def _handle_ws_message(self, requestId, text_data_json: dict=None, bytes_data=None):
        try:
            return self.send(text_data=json.dumps(self.__handlers[text_data_json['type']](requestId, text_data_json)))
        except Exception as err:
            Log.exception('_handle_ws_message err:[' + str(err) + ']')
        return self.send(text_data=json.dumps(IoTErrorResponse.GenJson(requestId=requestId)))
