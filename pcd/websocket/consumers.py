import json
import logging
import re

from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from pcd.config import iWebServerConfig
from pcd.models import DeviceInfo
from pcd.utils.device_utils import DeviceHTTPRequestUtil
from websocket.consumers import iWebServerConsumer

Log = logging.getLogger(__name__)


class PCDConsumer(iWebServerConsumer):
    def __init__(self):
        super().__init__()
        self.__handlers = {
            'container_status': self.__container_status,
            'container_create': self.__container_create,
            'container_destroy': self.__container_destroy
        }
        self.__device_util = DeviceHTTPRequestUtil()

    def __container_status(self, requestId, paras):
        try:
            device = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if(device == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not device.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)
            result = self._iot_util.InvokeThingService(subscribeTopicList=[f'/sys/{device.productKey}/{device.deviceName}/rrpc/response/webrtc/status/get'],
                                                       publishTopic=f'/sys/{device.productKey}/{device.deviceName}/rrpc/request/webrtc/status/get',
                                                       paras={},
                                                       timeout_s=10)
            if(result != None):
                return IoTSuccessResponse().GenJson(data={'deviceId': device.id, 'deviceStatus': 'ONLINE', 'publisherId': result['publisherId'], 'privateId': result['privateId'], 'roomId': result['roomId'], 'roomJoinPin': result['roomJoinPin']}, requestId=requestId)
            return IoTSuccessResponse().GenJson(data={'deviceId': device.id, 'deviceStatus': 'OFFLINE', 'publisherId': None, 'privateId': None, 'roomId': None, 'roomJoinPin': None}, requestId=requestId)
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
            result = self.__device_util.destroy_container(device)
            if (result == True):
                return IoTSuccessResponse().GenJson(requestId=requestId)
            return IoTErrorResponse.GenJson(error_msg='destroy container failed', requestId=requestId)
        except Exception as err:
            Log.exception('__container_destroy err:[' + str(err) + ']')
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
                    info = json.loads(msg)['RmsResult']['extras']['webrtc']
                    return self.send(text_data=json.dumps({'deviceId': device.id, 'deviceStatus': 'ONLINE', 'publisherId': info['publisherId'], 'privateId': info['privateId']}))
        except Exception as err:
            Log.exception('_on_mqtt_msg_cb err:[' + str(err) + ']')

        self.send(msg)

    def _handle_ws_message(self, requestId, text_data_json: dict=None, bytes_data=None):
        try:
            return self.send(text_data=json.dumps(self.__handlers[text_data_json['type']](requestId, text_data_json)))
        except Exception as err:
            Log.exception('_handle_ws_message err:[' + str(err) + ']')
        return self.send(text_data=json.dumps(IoTErrorResponse.GenJson(requestId=requestId)))
