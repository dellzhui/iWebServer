import json
from interface.utils.log_utils import loggerr
import re
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from pcd.config import iWebServerConfig
from pcd.datatype.datatype import WebsocketDeviceStatusDataType, WebsocketMeetingInfoDataType
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
            'container_meeting_status': self.__container_metting_status,
            'container_meeting_join': self.__container_meeting_join,
            'container_meeting_exit': self.__container_meeting_exit,
        }
        self.__device_util = DeviceHTTPRequestUtil()
        self.__webrtc_util = WebRTCUtil()
        self.__meeting_control_util = DeviceHTTPRequestUtil(base_url=iWebServerConfig.IWEBSERVER_DEVICE_MEETING_CONTRIL_BASE_URL)

    # https://www.wolai.com/yang_ids/bg4kyCjfdMqSza4qc7tTvF#vKWvkteTSSWpva36EedSqU
    def __container_status(self, requestId, paras):
        try:
            device = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if(device == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not device.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)

            device_webrtc_connection_info_container = self.__webrtc_util.get_device_webrtc_connection_info(device)
            if(device_webrtc_connection_info_container != None):
                data = WebsocketDeviceStatusDataType(device=device, deviceStatus='ONLINE')
                data.update_from_device_webrtc_connection_info(device_webrtc_connection_info_container)
                return IoTSuccessResponse().GenJson(data=data.to_dict(), requestId=requestId)
            return IoTSuccessResponse().GenJson(data=WebsocketDeviceStatusDataType(device=device, deviceStatus='OFFLINE').to_dict(), requestId=requestId)
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

    def __container_metting_status(self, requestId, paras):
        try:
            device = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if (device == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not device.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)

            device_meeting_infos = self.__meeting_control_util.get_meeting_infos(email=self._user.email)
            if(device_meeting_infos == None):
                return IoTErrorResponse.GenJson(requestId=requestId, error_msg='got meeting infos failed')

            meeting_infos = []
            for item in device_meeting_infos:
                websocket_meeting_info = WebsocketMeetingInfoDataType(device=device)
                if(websocket_meeting_info.update_from_request_result(item)):
                    meeting_infos.append(websocket_meeting_info.to_dict())
            return IoTSuccessResponse().GenJson(data=meeting_infos, requestId=requestId)
        except Exception as err:
            Log.exception('__container_metting_status err:[' + str(err) + ']')
        return IoTErrorResponse.GenJson(requestId=requestId)

    def __container_meeting_join(self, requestId, paras):
        try:
            device = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if (device == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not device.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)

            meeting_id = paras['meetingId']
            device_meeting_infos = self.__meeting_control_util.get_meeting_infos(email=self._user.email, meeting_id=meeting_id)
            if(device_meeting_infos == None or device_meeting_infos == []):
                return IoTErrorResponse.GenJson(requestId=requestId, error_msg='got meeting infos failed')

            # TODO: all meeting IDs are currently the same
            meeting_info = device_meeting_infos[0]

            device_webrtc_connection_info_container = self.__webrtc_util.get_device_webrtc_connection_info(device)
            if (device_webrtc_connection_info_container == None):
                Log.error('container not online')
                return IoTErrorResponse.GenJson(requestId=requestId, error_msg='container not online')

            websocket_meeting_info = WebsocketMeetingInfoDataType(device=device)
            if(not websocket_meeting_info.update_from_request_result(meeting_info)):
                Log.error('update meeting info failed')
                return IoTErrorResponse.GenJson(requestId=requestId)

            if (device_webrtc_connection_info_container.roomId == websocket_meeting_info.meetingRoomId):
                Log.error('already joined')
                return IoTErrorResponse.GenJson(requestId=requestId, error_msg='already joined')

            if(self.__webrtc_util.container_join_to_room(container=device, roomId=websocket_meeting_info.meetingRoomId, roomJoinPin=websocket_meeting_info.meetingRoomJoinPin)):
                device.meetingRunning = True
                device.meetingId = meeting_id
                device.meetingUrl = websocket_meeting_info.meetingUrl
                device.save()
                return IoTSuccessResponse().GenJson(data='join succeed', requestId=requestId)
            return IoTErrorResponse.GenJson(requestId=requestId, error_msg='join failed')
        except Exception as err:
            Log.exception('__container_meeting_join err:[' + str(err) + ']')
        return IoTErrorResponse.GenJson(requestId=requestId)

    def __container_meeting_exit(self, requestId, paras):
        try:
            device = DeviceInfo.objects.filter(id=paras['deviceId'], owner_id=self._user.id).last()
            if (device == None):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device not presenced', requestId=requestId)
            if (not device.is_container()):
                return IoTErrorResponse.GenJson(error_code=iWebServerConfig.IWEBSERVER_ERROR_CODE_DEVICE_NOT_PRESENCED, error_msg='device is not container', requestId=requestId)

            meeting_id = paras['meetingId']
            device_meeting_infos = self.__meeting_control_util.get_meeting_infos(email=self._user.email, meeting_id=meeting_id)
            if(device_meeting_infos == None or device_meeting_infos == []):
                return IoTErrorResponse.GenJson(requestId=requestId, error_msg='got meeting infos failed')

            # TODO: all meeting IDs are currently the same
            meeting_info = device_meeting_infos[0]

            device_webrtc_connection_info_container = self.__webrtc_util.get_device_webrtc_connection_info(device)
            if (device_webrtc_connection_info_container == None):
                Log.error('container not online')
                return IoTErrorResponse.GenJson(requestId=requestId, error_msg='container not online')

            websocket_meeting_info = WebsocketMeetingInfoDataType(device=device)
            if(not websocket_meeting_info.update_from_request_result(meeting_info)):
                Log.error('update meeting info failed')
                return IoTErrorResponse.GenJson(requestId=requestId)

            if (device_webrtc_connection_info_container.roomId != websocket_meeting_info.meetingRoomId):
                Log.error('not joined')
                return IoTErrorResponse.GenJson(requestId=requestId, error_msg='not joined')

            if(self.__webrtc_util.container_join_to_room(container=device, roomId=device.room.roomId, roomJoinPin=device.room.roomJoinPin)):
                device.meetingRunning = False
                device.save()
                return IoTSuccessResponse().GenJson(data='exit succeed', requestId=requestId)
            return IoTErrorResponse.GenJson(requestId=requestId, error_msg='exit failed')
        except Exception as err:
            Log.exception('__container_meeting_exit err:[' + str(err) + ']')
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
                    data = WebsocketDeviceStatusDataType(device=device, deviceStatus='ONLINE')
                    data.update_from_ready_event(msg)
                    return self.send(text_data=data.to_json())
        except Exception as err:
            Log.exception('_on_mqtt_msg_cb err:[' + str(err) + ']')

    def _handle_ws_message(self, requestId, type: str, paras=None, bytes_data=None):
        try:
            return self.send(text_data=json.dumps(self.__handlers[type](requestId, paras)))
        except Exception as err:
            Log.exception('_handle_ws_message err:[' + str(err) + ']')
        return self.send(text_data=json.dumps(IoTErrorResponse.GenJson(requestId=requestId)))
